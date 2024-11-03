from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile-update'),
    path('profile/delete/', views.profile_delete_view, name='profile-delete'),
    path('register/', views.register_view, name='register'),
    path('update_user_role/<int:user_id>/', views.update_user_role_view, name='update_user_role'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('user_management_users/', views.user_management_users_view, name='user_management_users'),
    path('user_management_dashboard/', views.user_management_dashboard_view, name='user_management_dashboard'),
    
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:property_id>/', views.property_detail, name='property_detail'),
    path('properties/add/', views.property_create, name='property_create'),
    path('properties/edit/<int:property_id>/', views.property_edit, name='property_edit'),
    path('my-properties/', views.seller_property_list, name='seller_property_list'),
    path('property/delete/<int:property_id>/', views.property_delete, name='property_delete'),
    path('property_documents/<int:property_id>/', views.property_documents, name='property_documents'),
    path('documents/', views.document_list_view, name='document_list'),


    path('documents/edit/<int:document_id>/', views.edit_document_view, name='document_edit'),
    path('documents/delete/<int:document_id>/', views.delete_document_view, name='document_delete'),
    
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('seller_properties/', views.seller_property_list, name='seller_property_list'),
    path('property_buy/<int:property_id>/', views.property_buy, name='property_buy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)