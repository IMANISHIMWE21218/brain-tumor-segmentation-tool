from django import forms

from .models import Patient, PatientReport


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('created_on', 'doctor', 'result_image')


class ReportForm(forms.ModelForm):
    class Meta:
        model = PatientReport
        fields = ('doctor_comment',)


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
