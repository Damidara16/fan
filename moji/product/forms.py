from django import forms
from .models import Points

class SetPoint(forms.ModelForm):
    class Meta:
        model = Points
        fields = ('likes', 'comment')
