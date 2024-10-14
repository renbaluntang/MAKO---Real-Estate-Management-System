from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .forms import UserRegistrationForm, UpdateUserRoleForm
from .models import Role, User
from django.contrib.auth.decorators import login_required

# Home page
def home(request):
    return render(request, 'home.html')

# Register view
def register_view(request):
    roles = Role.objects.all()  # Fetch all roles from the database
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            role_id = request.POST.get('role')
            user.role = Role.objects.get(id=role_id)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form, 'roles': roles})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Password reset view
def password_reset_view(request):
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'password_reset.html', {'form': form})

# Profile page
def profile_view(request):
    # Logic for displaying user's profile details could be added here
    return render(request, 'profile.html')

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