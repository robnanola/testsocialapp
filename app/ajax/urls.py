from django.conf.urls import url, patterns
from .views import SetProfilePicAjaxView

urlpatterns = patterns('',
    url(r'^profile_picture/$', SetProfilePicAjaxView.as_view(), name='ajax_set_profile_picture'),
    
)

