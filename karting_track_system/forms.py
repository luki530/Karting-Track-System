from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from .models import *
from django.forms.models import inlineformset_factory

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
