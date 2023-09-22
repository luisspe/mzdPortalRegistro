from django import forms
from .models import SpecialEvent

class SpecialEventForm(forms.ModelForm):
    class Meta:
        model = SpecialEvent
        fields = '__all__'
