from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


class CartView(TemplateView):
    # store é o nome da pasta dentro de templates
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        quantity = 0
        total = 0
        try:
            cart = Cart.objects.get(cart_id=_cart_id(self.request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity

            freight_product = (10 * total) / 100  # calculando 10% do produto como frete_product
            grand_total = total + freight_product  # valor final do carrinho é total + frete
            context['total'] = total
            context['quantity'] = quantity
            context['cart_itens'] = cart_items
            context['freight_product'] = freight_product
            context['grand_total'] = grand_total

        except ObjectDoesNotExist:
            pass
        return context


# pega o id da sessao do navegador, no cache
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        # verifica no banco se tem um carrinho com a sessão atual
        # caso não tenha cria uma nova sessao e um novo carrinho de compras
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request),
        )
    cart.save()
    try:
        # PRIMEIRO ELE VERIFICA NO BANCO SE JÁ EXISTE ESTE PRODUTO PARA ESTE CARRINHO
        # CASO NÃO TENHA, INSERE O PRODUTO NO CARRINHO DE COMPRAS
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    return redirect('cart')

# SUBTRAINDO UM ITEM DO CARRINHO AO PRECIONAR O BOTAO ' - (MENOS)'
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

# REMOVENDO UM ITEM DO CARRINHO PELO BOTÃO
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')