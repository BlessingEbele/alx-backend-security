from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Block an IP address by adding it to the BlockedIP model"

    def add_arguments(self, parser):
        parser.add_argument(
            "ip_address",
            type=str,
            help="The IP address you want to block"
        )

    def handle(self, *args, **options):
        ip_address = options["ip_address"]

        # Check if IP already exists
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(
                f"⚠️ IP {ip_address} is already blocked."
            ))
        else:
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(
                f"✅ Successfully blocked IP: {ip_address}"
            ))
