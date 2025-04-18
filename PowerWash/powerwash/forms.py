from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    #account_type = forms.ChoiceField(widget=forms.TextInput, choices=['provider', 'customer'])
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your first name',
        'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your last name',
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Choose a username',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address',
        'class': 'form-control'
    }))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            'class': 'form-control',
            'autocomplete': 'new-password'  # Add this for better browser behavior
        }),
        min_length=6,
        max_length=8,
        help_text='Password must be 6-8 characters with an uppercase letter and special character.'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control',
            'autocomplete': 'new-password'  # Add this for better browser behavior
        }),
        min_length=6,
        max_length=8,
        help_text='Re-enter your password.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    # Custom password validation for password1
    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must include at least one uppercase letter.")

        if not any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password must include at least one special character.")

        if all(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password cannot consist solely of special characters.")

        return password

    # Custom clean_password2 to completely bypass validation
    def clean_password2(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")  # Directly fetch raw input

        # Debugging: Print passwords to ensure they are being captured
        print(f"Password 1 (cleaned): {password1}")
        print(f"Password 2 (raw input): {password2}")

        # Compare password2 with password1
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        return password2  # Always return raw input, no validation

# Password form with validation logic for a single password input
class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=8)

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must include at least one uppercase letter.")

        # Check for at least one special character
        if not any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password must include at least one special character.")

        # Ensure password is not made only of special characters
        if all(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password cannot consist solely of special characters.")

        return password

# Sign in form with basic username and password fields
class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Enter your password.')

    class Meta:
        model = User
        fields = ['username', 'password']

# User profile form with additional fields for managing user data
class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False, help_text='Write a short bio about yourself.')
    profile_picture = forms.ImageField(required=False, help_text='Upload a profile picture.')

    class Meta:
        model = User
        fields = ['bio', 'profile_picture']

# Form to update user email
class UserEmailUpdateForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, help_text='Enter a new email address.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email

# Form to change user password
class UserPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Enter your old password.')
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=8, required=True, 
                                    help_text='New password must be between 6 and 8 characters, including at least one uppercase letter and one special character.')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Confirm your new password.')

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")

        # Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must include at least one uppercase letter.")

        # Check for at least one special character
        if not any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password must include at least one special character.")

        # Ensure password is not made only of special characters
        if all(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password):
            raise forms.ValidationError("Password cannot consist solely of special characters.")

        return password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_new_password')

        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")
        
        return confirm_password

class CreateServicesForm(forms.Form):
    name = forms.CharField(label='Service Name', max_length=100)
    description = forms.CharField(label='Service Description', max_length=100)
    price = forms.DecimalField(label='Service Price', max_digits=10, decimal_places=2)
