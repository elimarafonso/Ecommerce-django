from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

import carts.views
from category.models import Category
from carts.models import CartItem, Cart
from .models import Product


# Create your views here.


class StoreView(TemplateView):

    template_name = 'store/store.html'

    def get_context_data(self,  **kwargs):
        context = super(StoreView, self).get_context_data(**kwargs)

        category_slug = kwargs.get('category_slug')
        # se Category_slug não for NONE é porque tem um slug
        if  category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            context['products'] = Product.objects.all().filter(category=categories, is_available=True)
            context['quant_products'] = context['products'].count()
        else:
            context['categories'] = Category.objects.all()
            context['products'] = Product.objects.all().filter(is_available=True)
            context['quant_products'] = context['products'].count()

        return context


class ProductDetailView(TemplateView):
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        category_slug = kwargs.get('category_slug')
        product_slug = kwargs.get('product_slug')
        try:
            single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(product=single_product, cart__cart_id=carts.views._cart_id(self.request)).exists()
        except Exception as e:
            raise e

        context['product'] = single_product
        context['in_cart'] = in_cart
        return context
















