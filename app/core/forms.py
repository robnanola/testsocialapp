from django import forms
from app.core.models import UserProfile, Photo, WallItem

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['address', 'phone', 'work', 'education']


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['original_image',]


class WallPostForm(forms.ModelForm):

    class Meta:
        model = WallItem
        fields = ['content',]



class SearchForm(forms.Form):
    search = forms.CharField(required=False, max_length=100)