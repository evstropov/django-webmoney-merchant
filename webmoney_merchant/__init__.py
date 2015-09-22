__version__ = '1.0.3'
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'webmoney_merchant.Config'


class Config(AppConfig):
    name = 'webmoney_merchant'
    verbose_name = _("WebMoney Merchant")
    label = 'webmoney_merchant'
