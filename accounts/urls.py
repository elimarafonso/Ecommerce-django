from django.urls import path

from .views import RegisterFormView, LoginView, LogoutView, ForgotPasswordView, ResetPasswordFormView
from .views import DashboardView, UpdateAddressView, ListAddressView, CreateAddressView, DeleteAddressView
from . import views


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('createAddress/', CreateAddressView.as_view(), name='createAddress'),
    path('updateAddress/<int:pk>/', UpdateAddressView.as_view(), name='updateAddress'),
    path('deleteAddress/<int:pk>/', DeleteAddressView.as_view(), name='deleteAddress'),

    path('listAddress/', ListAddressView.as_view(), name='listAddress'),

    path('activate/<uidb64>/<token>/', views.Activate, name='activate'),
    path('forgotPassword/', ForgotPasswordView.as_view(), name='forgotPassword'),

    path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetPassword_validate'),
    path('resetPassword/', ResetPasswordFormView.as_view(), name='resetPassword'),
]