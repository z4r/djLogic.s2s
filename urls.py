from django.conf.urls.defaults import *

urlpatterns = patterns('s2s.views',
    (r'^publish/(?P<user>[^/]+)/(?P<partner_id>\w{2}_\d+_\d+_\d+)/(?P<click_id>[^/]+)/$', 'publish'),
    (r'^check_status/(?P<partner_id>\w{2}_\d+_\d+_\d+)/$', 'check_status'),
)

