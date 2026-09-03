from django import forms
from .models import Usuario

class userRegistrationForm(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email

class userLoginForm(forms.Form):
    username = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput())
    