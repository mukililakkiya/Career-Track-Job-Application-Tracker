from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            'company_name',
            'job_role',
            'location',
            'applied_date',
            'status',
            'job_link',
            'notes'
        ]

        widgets = {
            'applied_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }