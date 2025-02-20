from django import forms
from django.contrib.auth.models import User

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=8)

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must include at least one uppercase letter.")

        if not any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password must include at least one special character.")

        if all(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password cannot consist solely of special characters.")

        return password

class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
