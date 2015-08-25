from django import forms

from timereg.models import Shift

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['start_time','end_time']
    

class ExtendedShiftForm(forms.Form):
    pass
