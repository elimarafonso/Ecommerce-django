from django.urls import path

from .views import RegisterFormView, LoginView, LogoutView, DashboardView, ForgotPasswordView, ResetPasswordFormView
from . import views


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('activate/<uidb64>/<token>/', views.Activate, name='activate'),
    path('forgotPassword/', ForgotPasswordView.as_view(), name='forgotPassword'),

    path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetPassword_validate'),
    path('resetPassword/', ResetPasswordFormView.as_view(), name='resetPassword'),
]