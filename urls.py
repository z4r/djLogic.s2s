from django.conf.urls.defaults import *

urlpatterns = patterns('s2s.views',
    (r'^publish/(?P<partner_id>\w{2}_\d+_\d+_\d+)/(?P<click_id>[^/]+)/$', 'publish'),
    (r'^publish/check/(?P<partner_id>\w{2}_\d+_\d+_\d+)/(?P<click_id>[^/]+)/$', 'publish', { 'check' : True, }),
)

