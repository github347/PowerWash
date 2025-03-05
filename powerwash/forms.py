from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,
                                #   help_text='First name'
                                  )
    last_name = forms.CharField(max_length=30, required=True,
                                #  help_text='Last name'
                                 )
    email = forms.EmailField(max_length=254, required=True, 
                            #  help_text='Email address'
                             )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(max_length=254, required=True)
#     password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=8)
    
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

#     def clean_password(self):
#         password = self.cleaned_data.get("password1")

#         if not any(char.isupper() for char in password):
#             raise forms.ValidationError("Password must include at least one uppercase letter.")

#         if not any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
#             raise forms.ValidationError("Password must include at least one special character.")

#         if all(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
#             raise forms.ValidationError("Password cannot consist solely of special characters.")

#         return password

# class SignInForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'password']

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
