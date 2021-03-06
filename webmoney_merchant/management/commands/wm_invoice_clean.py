from optparse import make_option
from django.core.management.base import BaseCommand
from webmoney_merchant.models import Invoice


class Command(BaseCommand):
    help = "Clean unpaid invoices older than 'n' day."
    option_list = BaseCommand.option_list + (
        make_option('--days', '-d', default=3, action='store', type='int', dest='days', help='period of days'),
    )

    def handle(self, *labels, **options):
        Invoice.remove_old(options['days'])
