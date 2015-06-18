from datetime import datetime, timedelta
from django.core.management.base import NoArgsCommand
from webmoney_merchant.models import Invoice


class Command(NoArgsCommand):
    help = "Clean unpaid invoices older than one day."
    
    def handle_noargs(self, **options):
        Invoice.objects.filter(created_on__lt=datetime.utcnow()-timedelta(days=1), payment__isnull=True).delete()
