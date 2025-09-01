from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    """
    Detects suspicious IPs:
    - More than 100 requests in the last hour
    - Accessing sensitive paths (/admin, /login)
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1. Detect high frequency requests
    ip_counts = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(count=models.Count("id"))
        .filter(count__gt=100)
    )

    for entry in ip_counts:
        ip = entry["ip_address"]
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="Exceeding 100 requests in the last hour",
        )

    # 2. Detect access to sensitive paths
    sensitive_paths = ["/admin", "/login"]
    suspicious_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago, path__in=sensitive_paths
    )

    for log in suspicious_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed sensitive path: {log.path}",
        )
