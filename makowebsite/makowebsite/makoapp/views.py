

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegistrationForm, UpdateUserRoleForm, UserUpdateForm
from .models import Role, User,Property, TransactionHistory, Document
from django.contrib.auth import views as auth_views
from .forms import PropertyForm, DocumentForm, TransactionHistoryForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import PropertyUpdateForm 

    
def user_management(request):
    users = User.objects.all()
    return render(request, 'user_management_users.html', {'users': users})

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
                return redirect('home')
            else:
                print("Authentication failed")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)  # Use CustomLoginForm
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)  # Log the user in
                next_url = request.POST.get('next') or request.GET.get('next') or 'home'
                return redirect(next_url)  # Redirect to the next URL or home
            else:
                form.add_error(None, "Invalid username or password.")  # Add error if authentication fails
    else:
        form = CustomLoginForm()  # Initialize the form for GET requests

    return render(request, 'login.html', {'form': form, 'next': request.GET.get('next', '')})


@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user_profile': user_profile})

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)
            user.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('profile', user_id=request.user.id)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your account has been deleted successfully')
        return redirect('profile')
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

def user_management_users_view(request):
    # Get search query and role filter from request
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', 'all')

    # Base query for users
    users = User.objects.exclude(role__role_name='Admin')  # Exclude admin users

    # Apply search filter
    if search_query:
        users = users.filter(user_name__icontains=search_query)

    # Apply role filter
    if role_filter == 'buyer':
        users = users.filter(role__role_name='Buyer')
    elif role_filter == 'seller':
        users = users.filter(role__role_name='Seller')

    return render(request, 'user_management_users.html', {'users': users, 'search_query': search_query, 'role_filter': role_filter})


def user_management_dashboard_view(request):
    total_seller_accounts = User.objects.filter(role__role_name='Seller').count()
    total_buyer_accounts = User.objects.filter(role__role_name='Buyer').count()
    recent_property = Property.objects.filter(is_sold=False).order_by('-id').first()  # Most recent property
    recent_sold_property = Property.objects.filter(is_sold=True).order_by('-id').first()  # Most recent sold property
    total_properties = Property.objects.count()  # Total properties count
    total_sold_properties = Property.objects.filter(is_sold=True).count()  # Total sold properties count

    return render(request, 'user_management_dashboard.html', {
        'total_seller_accounts': total_seller_accounts,
        'total_buyer_accounts': total_buyer_accounts,
        'recent_property': recent_property,
        'recent_sold_property': recent_sold_property,
        'total_properties': total_properties,  # Pass the total properties count
        'total_sold_properties': total_sold_properties  # Pass the total sold properties count
    })

def property_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    # Base query for all properties
    properties = Property.objects.all()

    # Apply search filter
    if query:
        properties = properties.filter(property_name__icontains=query)

    # Apply status filter
    if status == 'sold':
        properties = properties.filter(is_sold=True)
    elif status == 'unsold':
        properties = properties.filter(is_sold=False)

    return render(request, 'property_list.html', {'properties': properties, 'query': query})

@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'property_detail.html', {'property': property})




@login_required
def property_create(request):
    form = PropertyForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            property = form.save(commit=False)  # Create a Property instance but don't save it yet
            property.seller = request.user      # Assign the current user as the seller
            
            # Set the buyer based on the form input
            property.buyer = form.cleaned_data.get('buyer')  # Assign the selected buyer
            
            # Save the property instance
            property.save()                     # Now save the instance
            return redirect('seller_property_list')  # Redirect to the seller's property list

    return render(request, 'property_form.html', {'form': form})




@login_required
def property_edit(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    form = PropertyUpdateForm(request.POST or None, request.FILES or None, instance=property_instance)

    if request.method == 'POST':
        if form.is_valid():
            updated_property = form.save(commit=False)  # Create a Property instance but don't save it yet
            updated_property.seller = property_instance.seller  # Keep the original seller
            
            # Set the property status based on the form input
            updated_property.is_sold = form.cleaned_data.get('is_sold') == 'True'  # Set is_sold based on dropdown
            
            # Set the buyer based on the form input
            updated_property.buyer = form.cleaned_data.get('buyer')  # Assign the selected buyer
            
            # Clear the buyer information if the property is marked as unsold
            if not updated_property.is_sold:
                updated_property.buyer = None  # Disassociate the buyer from the property
            
            updated_property.save()  # Now save the instance
            return redirect('seller_property_list')  # Redirect to the seller's property list

    return render(request, 'property_update_seller.html', {'form': form, 'property': property_instance})


@login_required
def property_delete(request, property_id):
    property = get_object_or_404(Property, id=property_id, seller=request.user)
    if request.method == 'POST':
        property.delete()
        return redirect('seller_property_list')
    return render(request, 'property_confirm_delete.html', {'property': property})

@login_required
def document_list_view(request):
    # Assuming the seller is the logged-in user
    seller = request.user
    properties = Property.objects.filter(seller=seller)
    return render(request, 'document_list.html', {'properties': properties})


@login_required
def transaction_list(request):
    transactions = TransactionHistory.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})




@login_required(login_url='login')  # Replace 'login' with your actual login URL name
def seller_property_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    # Base query for properties belonging to the current user
    properties = Property.objects.filter(seller=request.user)

    # Apply search filter
    if query:
        properties = properties.filter(property_name__icontains=query)

    # Apply status filter
    if status == 'sold':
        properties = properties.filter(is_sold=True)
    elif status == 'unsold':
        properties = properties.filter(is_sold=False)

    return render(request, 'seller_property_list.html', {'properties': properties, 'query': query})


@login_required
def property_buy(request, property_id):
    property = get_object_or_404(Property, id=property_id, is_sold=False)

    # Assign the buyer and mark the property as sold
    property.buyer = request.user
    property.is_sold = True
    property.save()

    # Create a transaction history record
    TransactionHistory.objects.create(
        transaction_date=timezone.now(),
        transaction_desc=f"Property {property.property_name} purchased",
        seller=property.seller,
        buyer=request.user,
        property=property
    )

    # Update or create a document for the transaction
    Document.objects.update_or_create(
        property=property,
        defaults={'buyer': request.user, 'seller': property.seller}
    )

    # Redirect to a confirmation page or the property detail page
    return redirect('property_detail', property_id=property.id)

def property_documents(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    documents = Document.objects.filter(property=property)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.property = property
            document.save()
            return redirect('property_documents', property_id=property.id)
    else:
        form = DocumentForm()

    return render(request, 'property_documents.html', {
        'property': property,
        'documents': documents,
        'form': form
    })
    
    
def edit_document_view(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('property_documents', property_id=document.property.id)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'edit_document.html', {'form': form, 'document': document})

def delete_document_view(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    property_id = document.property.id
    if request.method == 'POST':
        document.delete()
        return redirect('property_documents', property_id=property_id)
    return render(request, 'delete_document.html', {'document': document})
 


@login_required
def buyer_property_list(request):
    if request.user.is_authenticated:
        properties = Property.objects.filter(buyer=request.user)  # Assuming you have a buyer field in Property
    else:
        properties = None

    return render(request, 'buyer_properties.html', {'properties': properties})