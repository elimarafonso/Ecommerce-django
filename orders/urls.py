from django.urls import path
from .views import PlaceOrderView, PaymentView

urlpatterns = [
    path('place_order/', PlaceOrderView.as_view(), name='placeOrder'),
    path('payment/', PaymentView.as_view(), name='payment'),
]