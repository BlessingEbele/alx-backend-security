from django.db import models
from django.utils import timezone


# Create your models here.

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    visit_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.ip_address
    
class VisitLog(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Visit from {self.ip_address} at {self.visit_time}"
    
class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    blocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.ip_address

class IPGeolocation(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    isp = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Geolocation for {self.ip_address}"

class IPReputation(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    reputation_score = models.IntegerField(default=0)
    last_checked = models.DateTimeField(auto_now=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reputation for {self.ip_address}: {self.reputation_score}"

class IPAccessLog(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    accessed_url = models.URLField()
    response_status = models.PositiveIntegerField()

    def __str__(self):
        return f"Access log for {self.ip_address} at {self.access_time}"

class IPBlacklist(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.ip_address


class IPActivitySummary(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    total_visits = models.PositiveIntegerField(default=0)
    total_accesses = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Activity summary for {self.ip_address}"
    
class IPThreatLevel(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    threat_level = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='low')
    assessed_at = models.DateTimeField(auto_now=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Threat level for {self.ip_address}: {self.threat_level}"  
    
class IPUsagePattern(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    pattern_description = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Usage pattern for {self.ip_address}"   

class IPNotification(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.ip_address} - {self.notification_type}"

class IPDeviceInfo(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device info for {self.ip_address}"

class IPConnectionType(models.Model):   
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    connection_type = models.CharField(max_length=100, blank=True, null=True)
    isp = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Connection type for {self.ip_address}"
    
class IPSession(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Session for {self.ip_address} starting at {self.session_start}"
    
class IPErrorLog(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    error_time = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField()
    stack_trace = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Error log for {self.ip_address} at {self.error_time}"  
    

class IPReferral(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    referral_url = models.URLField()
    referred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral for {self.ip_address} from {self.referral_url}"

class IPCampaignTracking(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    tracked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Campaign tracking for {self.ip_address} - {self.campaign_name}"
    
class IPAnomalyDetection(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    anomaly_type = models.CharField(max_length=100)
    detected_at = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Anomaly detection for {self.ip_address} - {self.anomaly_type}"
    
class IPDataUsage(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    data_sent = models.BigIntegerField(default=0)  # in bytes
    data_received = models.BigIntegerField(default=0)  # in bytes
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data usage for {self.ip_address} at {self.recorded_at}"
    
class IPGeofencing(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    allowed_countries = models.TextField(help_text="Comma-separated country codes")
    blocked_countries = models.TextField(help_text="Comma-separated country codes")
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Geofencing for {self.ip_address}"
    
class IPBehavioralAnalysis(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    behavior_pattern = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Behavioral analysis for {self.ip_address}"
    
class IPThreatIntelligence(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    threat_source = models.CharField(max_length=100)
    threat_details = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Threat intelligence for {self.ip_address} from {self.threat_source}"
    
class IPReputationHistory(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    reputation_score = models.IntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reputation history for {self.ip_address} at {self.changed_at}"
    
class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.TextField()
    flagged_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"

class IPThreatSource(models.Model):
    ip_address = models.OneToOneField(IPAddress, on_delete=models.CASCADE)
    threat_source = models.CharField(max_length=100, blank=True, null=True)
    threat_level = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='low')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Threat source for {self.ip_address}: {self.threat_source}"

