from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# Example login view with rate limiting
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method == "POST":
        # Example placeholder logic
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Normally you'd authenticate with Django's auth system
        if username == "admin" and password == "password123":
            return JsonResponse({"message": "Login successful!"})
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "POST request required"}, status=400)
