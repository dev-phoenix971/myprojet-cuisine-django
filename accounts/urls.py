from django.urls import path, include
from accounts import views
from accounts.views import login_view, logout_view, profile_page, add_photo, change_photo, password_reset_request, passwordResetConfirm, password_reset_complete


app_name = "accounts"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('profile/', profile_page, name='profile'),
    path('create/', views.CreateProfile.as_view(), name="create_profile"),
    path('edite/<int:pk>/update/', views.UpdateProfile.as_view(), name="edite_profile"),
    path("change-profile-image/", add_photo, name="add_photo"),
    path("change-picture/", change_photo, name="change_photo"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_complete/', views.account_activation_complete, name='account_activation_complete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', password_reset_request, name='password_reset_request'),
    path('reset/<uidb64>/<token>', passwordResetConfirm, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete, name='password_reset_complete'),
    path('confidentialite/', views.confidentialite, name="confidentialite"),
]    