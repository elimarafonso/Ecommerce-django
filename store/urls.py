from django.urls import path
from .views import StoreView, ProductDetailView, SearchListView


urlpatterns = [
    path('', StoreView.as_view(), name='store'),
    path('category/<slug:category_slug>/', StoreView.as_view(), name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='ProductDetail'),
    path('search/', SearchListView.as_view(), name='search'),
]