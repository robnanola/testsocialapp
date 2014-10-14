from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib import admin

from app.core.views import SearchView, HomeView

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
    url(r'^accounts/password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),


    # *************************************************
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^search/$', SearchView.as_view(), name='search'),

    #(r'^comments/', include('django_comments.urls')),
    (r'^profile/', include('app.core.urls')),
    (r'^ajax/', include('app.ajax.urls')),
    (r'^user/', include('app.wall.urls')),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    #url(r'^profile/$', 'app.core.views.profile', name='profile'),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
