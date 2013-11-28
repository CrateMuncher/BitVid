from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^login', 'main.views.login', name='login'),
    url(r'^signup', 'main.views.signup', name='signup'),
    url(r'^logout', 'main.views.logout', name='logout')
    # Examples:
    # url(r'^$', 'bitvid.views.home', name='home'),
    # url(r'^bitvid/', include('bitvid.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()