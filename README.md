
````markdown
# ALX Backend Security – IP Tracking & Anomaly Detection

This project is part of the **ALX Backend Security** track.  
It provides tools for **IP request tracking, anomaly detection, and blocking suspicious IPs** in a Django project.

---

## 🚀 Features
- Middleware to log incoming IP requests.
- Integration with geolocation services for IP enrichment.
- **Celery tasks** for anomaly detection (e.g., too many requests, sensitive path access).
- Custom Django **management command** to block suspicious IPs.

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/BlessingEbele/alx-backend-security.git
   cd alx-backend-security
````

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Project

1. Apply migrations:

   ```bash
   python manage.py migrate
   ```

2. Start the development server:

   ```bash
   python manage.py runserver
   ```

3. (Optional) Run Celery worker and beat scheduler:

   ```bash
   celery -A security_project worker -l info
   celery -A security_project beat -l info
   ```

---

## 🔒 Blocking Suspicious IPs

The project comes with a **custom management command** for blocking suspicious IPs flagged by anomaly detection.

Run:

```bash
python manage.py block_ip
```

This will:

* Check the `SuspiciousIP` model.
* Block all flagged IPs (based on your defined rules).

---

## 🛠 Development

For local development, you can use:

```bash
pip install -r requirements-dev.txt
```

---

## 📄 License

This project is part of the ALX Backend curriculum.
Free to use for learning purposes.


