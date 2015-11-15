from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^scrape/$', 'scrape.views.query'),
    url(r'^$', 'main.views.index'),
    url(r'^search/$', 'main.views.search'),
    url(r'^register/$', 'main.views.register'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^about/$', 'main.views.about'),
    url(r'^subscribe/(.+)/$', 'main.views.subscribe'),
    url(r'^unsubscribe/(.+)/$', 'main.views.unsubscribe'),
    url(r'^privacy/$', 'main.views.privacy'),
    url(r'^contact/$', 'main.views.contact'),
    url(r'^keyworddump/$', 'main.views.keyworddump'),
    url(r'^keyworddump/csv/$', 'main.views.keywordcsv'),
    url(r'^stats/$', 'main.views.stats'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
