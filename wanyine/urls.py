from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from home.views import GuaranteeView, login_required

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('home.views',
    url(r'^$', 'home', name = 'home'),
    url(r'^accounts/login/', 'login'),
    url(r'^guarantee/(\d+)/', login_required(GuaranteeView.as_view()), name = 'guarantee'),
    url(r'^(\w+)/$', 'invoke'),
    # Examples:
    #url(r'^release/', 'home.views.release', name='home'),
    # url(r'^wanyine/', include('wanyine.foo.urls')),
)
