from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .forms import UserRegistrationForm, UpdateUserRoleForm
from .models import Role, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse



def user_management(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'user_management_users.html', {'users': users})

# Home page
def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('user_management_dashboard')  # Redirect to the new dashboard
            else:
                print("Authentication failed")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_management_dashboard')  # Redirect to the new dashboard
            else:
                print("Authentication failed")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Password reset view
def password_reset_view(request):
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'password_reset.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def profile_update_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'profile_update.html', {'form': form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    return render(request, 'profile_delete.html')



@login_required
def update_user_role_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UpdateUserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = UpdateUserRoleForm(instance=user)
    return render(request, 'update_user_role.html', {'form': form, 'user': user})


def user_management_users_view(request):
    return render(request, 'user_management_users.html')

def user_management_dashboard_view(request):
    return render(request, 'user_management_dashboard.html')