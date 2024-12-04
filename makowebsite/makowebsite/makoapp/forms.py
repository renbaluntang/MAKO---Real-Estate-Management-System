from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import User, Role, Property, Document, TransactionHistory, PropertyImage


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=255,
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control max-width-input'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control max-width-input'})
    )
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
    username = forms.CharField(
        max_length=255,
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control max-width-input'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control max-width-input'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control max-width-input'})
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

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Exclude the 'Admin' role from the choices
        self.fields['role'].queryset = Role.objects.exclude(role_name='Admin')

    def clean(self):
        cleaned_data = super().clean()
        user_password = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if user_password and password2 and user_password != password2:
            self.add_error('password2', "The two password fields didn’t match.")

        return cleaned_data

class UpdateUserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(), 
        required=True,
        widget=forms.Select(attrs={'class': 'form-control max-width-input', 'placeholder': 'Select Role'})
    )

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
    user_image = forms.ImageField(
        required=False, 
        label='Profile Image', 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control max-width-input'})
    )
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

    class Meta:
        model = User
        fields = ['user_name', 'user_contact', 'user_email', 'user_address', 'user_image']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields didn’t match.")

        return cleaned_data
    
class PropertyUpdateForm(forms.ModelForm):
    PROPERTY_STATUS_CHOICES = [
        (False, 'Unsold'),
        (True, 'Reserved'),
    ]
    
    is_reserved = forms.ChoiceField(
        choices=PROPERTY_STATUS_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}), 
        required=False
    )
    
    buyer = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Use the custom User model
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Buyer"
    )

    class Meta:
        model = Property
        fields = ['property_name', 'property_description', 'property_price', 'property_image', 'is_reserved', 'buyer']
        widgets = {
            'property_name': forms.TextInput(attrs={'class': 'form-control'}),
            'property_description': forms.TextInput(attrs={'class': 'form-control'}),
            'property_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class PurchaseConfirmationForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    address = forms.CharField(max_length=255, label='Address', required=True)
    phone = forms.CharField(max_length=15, label='Phone Number', required=True)
    
    # Dummy field (not required)
    dummy_field = forms.CharField(max_length=100, label='Dummy Field', required=False, widget=forms.TextInput(attrs={'disabled': 'disabled'}))

    username = forms.CharField(max_length=150, label='Username', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add any custom validation logic for email here
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Add any custom validation logic for phone here
        return phone

class PropertyForm(forms.ModelForm):
    buyer = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Buyer"
    )

    class Meta:
        model = Property
        fields = ['property_name', 'property_description', 'property_price', 'property_image', 'buyer']  # Exclude seller
        widgets = {
            'property_name': forms.TextInput(attrs={'class': 'form-control'}),
            'property_description': forms.TextInput(attrs={'class': 'form-control'}),
            'property_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        self.seller = kwargs.pop('seller', None)  # Get the seller from kwargs
        super(PropertyForm, self).__init__(*args, **kwargs)
        if self.seller:
            self.fields['seller'] = forms.ModelChoiceField(
                queryset=User.objects.filter(id=self.seller.id),  # Set the seller to the current user
                initial=self.seller,
                widget=forms.HiddenInput()  # Optionally hide the seller field
            )

class TransactionHistoryForm(forms.ModelForm):
    class Meta:
        model = TransactionHistory
        fields = ['transaction_date', 'transaction_desc', 'seller', 'buyer', 'property']
        
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['documentation_type', 'documentation_image']
        widgets = {
            'documentation_type': forms.TextInput(attrs={'class': 'form-control'}),
            'documentation_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']