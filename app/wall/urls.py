from django.conf.urls import url, patterns
from .views import UserWallView, WallItemView

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9])/$', UserWallView.as_view(), name='user_wall'),
    url(r'^item/(?P<uuid>\w+)/$', WallItemView.as_view(), name='wall_item'),
    
)

