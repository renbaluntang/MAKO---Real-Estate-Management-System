from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role

class UserRegistrationForm(UserCreationForm):
    # Custom fields for user registration
    user_name = forms.CharField(max_length=100, label='Full Name')
    user_contact = forms.CharField(max_length=11, label='Contact Number')
    user_email = forms.EmailField(label='Email Address')
    user_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Address')
    user_image = forms.ImageField(required=False, label='Profile Image')
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label='Role')

    class Meta:
        model = User
        fields = ['user_name', 'user_contact', 'user_email', 'user_address', 'user_image', 'role', 'username', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'This field is required.',
                'max_length': 'Username must be 150 characters or fewer.',
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
        
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_name = self.cleaned_data['user_name']
        user.user_contact = self.cleaned_data['user_contact']
        user.user_email = self.cleaned_data['user_email']
        user.user_address = self.cleaned_data['user_address']
        user.user_image = self.cleaned_data.get('user_image', None)
        user.role = self.cleaned_data['role']

        if commit:
            user.save()

        return user


class UpdateUserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['role']