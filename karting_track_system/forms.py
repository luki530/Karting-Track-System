from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

class SignUpForm(UserCreationForm):  
        class Meta:  
            model = User  
            fields = ('email', 'username')
