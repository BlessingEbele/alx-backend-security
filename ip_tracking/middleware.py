from django.utils import timezone
from .models import RequestLog
import django_ip_geolocation


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract client IP
        ip_address = self.get_client_ip(request)
        path = request.path

        # Log request details
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=timezone.now(),
            path=path
        )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP address from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# To use this middleware, add 'ip_tracking.middleware.IPLoggingMiddleware' to MIDDLEWARE in settings.py 
# and ensure you have a RequestLog model defined in models.py to store the logs.    

# ip_tracking/middleware.py
import logging
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.core.cache import cache
from .models import RequestLog, BlockedIP


logger = logging.getLogger(__name__)

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geo_api = django_ip_geolocation("YOUR_API_KEY")  # replace with real API key

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # 1. Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            logger.warning(f"Blocked request from blacklisted IP: {ip}")
            return HttpResponseForbidden("Forbidden: Your IP is blacklisted")

        # 2. Fetch geolocation (with caching)
        geo_data = cache.get(ip)
        if not geo_data:
            try:
                response = self.geo_api.getGeolocation(ip_address=ip)
                geo_data = {
                    "country": response.get("country_name", ""),
                    "city": response.get("city", "")
                }
                cache.set(ip, geo_data, timeout=86400)  # cache 24h
            except Exception as e:
                logger.error(f"Geo lookup failed for IP {ip}: {e}")
                geo_data = {"country": "", "city": ""}

        # 3. Log the request with geolocation
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=now(),
            path=request.path,
            country=geo_data["country"],
            city=geo_data["city"]
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        """ Extract client IP from headers """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

# To use this middleware, add 'ip_tracking.middleware.IPTrackingMiddleware' to MIDDLEWARE in settings.py
# and ensure you have a BlockedIP model defined in models.py to manage blocked IPs.
# ip_tracking/middleware.py

from django.http import HttpResponseForbidden
from ip_tracking.models import BlockedIP

class BlockIPMiddleware:
    """
    Middleware to block requests from blacklisted IP addresses.
    Relies on django-ip-geolocation to detect client IP info.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Example: hardcoded blacklist, you can later store in DB
        self.blacklisted_ips = ["127.0.0.1"]  

    def __call__(self, request):
        # django-ip-geolocation adds `request.geolocation`
        client_ip = request.geolocation.get("ip", None) if hasattr(request, "geolocation") else None

        if client_ip in self.blacklisted_ips:
            return HttpResponseForbidden("Access Denied: Your IP is blocked.")

        return self.get_response(request)

# To use this middleware, add 'ip_tracking.middleware.BlockIPMiddleware' to MIDDLEWARE in settings.py
# and ensure you have a BlockedIP model defined in models.py to manage blocked IPs
# ip_tracking/middleware.py

import requests
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from .models import RequestLog

class GeoLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)

        # Check cache first
        cached_geo = cache.get(ip)
        if cached_geo:
            country, city = cached_geo
        else:
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}")
                data = response.json()
                if data["status"] == "success":
                    country = data.get("country", "")
                    city = data.get("city", "")
                    # Cache result for 24 hours
                    cache.set(ip, (country, city), 60 * 60 * 24)
                else:
                    country, city = "", ""
            except Exception:
                country, city = "", ""

        # Save request log
        RequestLog.objects.create(
            ip_address=ip,
            country=country,
            city=city
        )

    def get_client_ip(self, request):
        """Extract client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
# To use this middleware, add 'ip_tracking.middleware.GeoLoggingMiddleware' to MIDDLEWARE in settings.py
# and ensure you have a RequestLog model defined in models.py to store the logs.    

from .models import RequestLog

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        geo_data = getattr(request, "geo_data", {})
        RequestLog.objects.create(
            ip_address=request.META.get("REMOTE_ADDR"),
            city=geo_data.get("city"),
            country=geo_data.get("country"),
            path=request.path,
        )
        return response
