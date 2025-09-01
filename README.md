# alx-backend-securit
# IP Tracking Project

## Task 0: Basic IP Logging Middleware

### Overview
This task implements middleware to log the IP address, request path, and timestamp of every incoming HTTP request.

### Implementation
- **Model**: `RequestLog` in `ip_tracking/models.py`
  - Fields: `ip_address`, `timestamp`, `path`
- **Middleware**: `IPLoggingMiddleware` in `ip_tracking/middleware.py`
  - Logs incoming requests into the `RequestLog` model.
- **Settings**: Registered middleware in `settings.py`

### Usage
1. Run migrations:
   ```bash
   python manage.py makemigrations ip_tracking
   python manage.py migrate
y