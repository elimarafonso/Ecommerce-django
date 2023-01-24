from django.urls import path
from .views import StoreView, ProductDetailView


urlpatterns = [
    path('', StoreView.as_view(), name='store'),
    path('<slug:category_slug>/', StoreView.as_view(), name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='ProductDetail'),
]