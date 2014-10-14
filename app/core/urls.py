from django.conf.urls import url, patterns
from .views import (UpdateProfileView, ProfileView, 
    UpdateProfileFormView, UpdateProfilePicture)

urlpatterns = patterns('',
    url(r'^$',  ProfileView.as_view(), name='profile'),
    url(r'^update/$', UpdateProfileFormView.as_view(), name='profile_update'),
    url(r'^profile_picture/$', UpdateProfilePicture.as_view(), name='update_profile_picture'),
)

