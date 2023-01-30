from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import carts.views
from category.models import Category
from carts.models import CartItem
from .models import Product


class StoreView(TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super(StoreView, self).get_context_data(**kwargs)

        category_slug = kwargs.get('category_slug')
        # se Category_slug não for NONE é porque tem um slug
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)

            products_by_category = Product.objects.all().filter(category=categories, is_available=True).order_by('id')
            # paginando produtos por categorias
            paginator = Paginator(products_by_category, 1)
            page = self.request.GET.get('page')
            paged_products = paginator.get_page(page)
            context['products'] = paged_products
            #
            context['quant_products'] = products_by_category.count()
        else:
            context['categories'] = Category.objects.all()

            # paginando produtos
            products_all = Product.objects.all().filter(is_available=True).order_by('id')
            paginator = Paginator(products_all, 5)
            page = self.request.GET.get('page')
            paged_products = paginator.get_page(page)
            context['products'] = paged_products

            context['quant_products'] = products_all.count()

        return context


class ProductDetailView(TemplateView):
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        category_slug = kwargs.get('category_slug')
        product_slug = kwargs.get('product_slug')
        try:
            single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
            in_cart = CartItem.objects.filter(product=single_product,
                                              cart__cart_id=carts.views._cart_id(self.request)).exists()
        except Exception as e:
            raise e

        context['product'] = single_product
        context['in_cart'] = in_cart
        return context


class SearchListView(ListView):
    template_name = 'store/store.html'
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)

        # paginando produtos pesquisados

        if 'search_key' in self.request.GET and self.request.GET.get('search_key'):
            search_key = self.request.GET.get('search_key')
            products_search = Product.objects.all().filter(product_name__icontains=search_key, is_available=True).order_by('id')

            page = self.request.GET.get('page')
            search_key = self.request.GET.get('search_key')
            paginator = Paginator(products_search, 5)

            paged_products = paginator.get_page(page)

            context['products'] = paged_products
            context['search_key'] = search_key

            # numero de produtos encotrados na pesquisa
            context['quant_products'] = products_search.count()

        else:
            context['quant_products'] = 0
            context['search_key'] = ''
            context['products'] = ''

        return context
