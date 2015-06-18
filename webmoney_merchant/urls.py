from django.conf.urls import patterns, url

urlpatterns = patterns(
    'webmoney_merchant.views',
    url(r'^result/$', 'result', name='webmoney_result'),
    url(r'^success/$', 'success', name='webmoney_success'),
    url(r'^fail/$', 'fail', name='webmoney_fail'),
)
