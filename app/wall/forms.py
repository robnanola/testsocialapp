from django import forms
from app.core.models import WallItem


class WallPostForm(forms.ModelForm):

    class Meta:
        model = WallItem
        fields = ['content',]