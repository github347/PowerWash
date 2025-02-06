from django import forms
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
