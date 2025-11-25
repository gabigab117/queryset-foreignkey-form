from django import forms
from .models import Appointment, Animal


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'animal', 'reason']
        
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["animal"].queryset = Animal.objects.filter(owner=user)
    