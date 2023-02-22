from django.urls import path

from .views import RegisterFormView, LoginView, LogoutView


urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]