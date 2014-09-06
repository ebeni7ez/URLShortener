from django.conf.urls import patterns, include, url

urlpatterns = patterns('urls.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<short_url>\w+)$', 'redirect_short_url', name='redirect_short_url'),
)
