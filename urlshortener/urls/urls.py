from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('urls.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<short_url>\w+)$', 'redirect_short_url', name='redirect_short_url'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.STATIC_ROOT}),
)
