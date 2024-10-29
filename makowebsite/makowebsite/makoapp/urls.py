from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile-update'),
    path('profile/delete/', views.profile_delete_view, name='profile-delete'),
    path('register/', views.register_view, name='register'),
    path('update_user_role/<int:user_id>/', views.update_user_role_view, name='update_user_role'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('user_management_users/', views.user_management_users_view, name='user_management_users'),  # New URL
    path('user_management_dashboard/', views.user_management_dashboard_view, name='user_management_dashboard'),
]