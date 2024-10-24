# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role

class UserRegistrationForm(UserCreationForm):
    user_name = forms.CharField(
        max_length=255, 
        label='Full Name', 
        widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control max-width-input'})
    )
    user_contact = forms.CharField(
        max_length=20, 
        label='Contact Number', 
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number', 'class': 'form-control max-width-input'})
    )
    user_email = forms.EmailField(
        label='Email Address', 
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control max-width-input'})
    )
    user_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Address', 'class': 'form-control max-width-input'}), 
        label='Address'
    )
    user_image = forms.ImageField(
        required=False, 
        label='Profile Image', 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control max-width-input'})
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(), 
        required=True, 
        label='Role', 
        widget=forms.Select(attrs={'class': 'form-control max-width-input'})
    )

    class Meta:
        model = User
        fields = ['user_name', 'user_contact', 'user_email', 'user_address', 'user_image', 'role', 'username', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'This field is required.',
                'max_length': 'Username must be 255 characters or fewer.',
                'invalid': 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.',
            },
            'password1': {
                'required': 'This field is required.',
                'min_length': 'Password must contain at least 8 characters.',
                'password_too_similar': 'Your password can’t be too similar to your other personal information.',
                'password_too_common': 'Your password can’t be a commonly used password.',
                'password_entirely_numeric': 'Your password can’t be entirely numeric.',
            },
            'password2': {
                'required': 'This field is required.',
                'password_mismatch': 'The two password fields didn’t match.',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        user_password = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if user_password and password2 and user_password != password2:
            self.add_error('password2', "The two password fields didn’t match.")

        return cleaned_data

class UpdateUserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['role']

class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='New Password', 
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'form-control max-width-input'}),
        required=False
    )
    password2 = forms.CharField(
        label='Confirm New Password', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'form-control max-width-input'}),
        required=False
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control max-width-input'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['user_name', 'user_contact', 'user_email', 'user_address', 'user_image', 'role']