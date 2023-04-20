from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from accounts.models import Account, DeliveryAddress
from store.models import Product, Variation
from .models import Cart, CartItem
from accounts.forms import DeliveryAddressForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


class CartView(TemplateView):
    # store é o nome da pasta dentro de templates
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        quantity = 0
        total = 0
        user = self.request.user
        try:
            if self.request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=user, is_active=True)
            else:
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
    current_user = request.user
    product = Product.objects.get(id=product_id)
    product_list_variation = []

    # SE O USUÁRIO É AUTENTICADO?
    if current_user.is_authenticated:

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_list_variation.append(variation)
                except:
                    pass

        is_cart_items_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_items_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            # existe variação deste produto  ? -> no banco
            # variação atual do produto - > product_variation
            # item_id -> Banco
            exist_variation_list = []
            id = []

            for item in cart_item:
                exist_variation = item.variations.all()
                exist_variation_list.append(list(exist_variation))
                id.append(item.id)

            if product_list_variation in exist_variation_list:
                # incrementa a quantidade do item
                index = exist_variation_list.index(product_list_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # cria um novo produto com variaçao diferente
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_list_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_list_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )

            if len(product_list_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_list_variation)
            cart_item.save()

        return redirect('cart')
    #
    # SE O USUÁRIO NÃO É AUTENTICADO?
    #
    else:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_list_variation.append(variation)
                except:
                    pass

        try:
            # verifica no banco se tem um carrinho com a sessão atual
            # caso não tenha cria uma nova sessao e um novo carrinho de compras
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request),
            )
        cart.save()

        is_cart_items_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_items_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existe variação deste produto  ? -> no banco
            # variação atual do produto - > product_variation
            # item_id -> Banco
            exist_variation_list = []
            id = []

            for item in cart_item:
                exist_variation = item.variations.all()
                exist_variation_list.append(list(exist_variation))
                id.append(item.id)

            if product_list_variation in exist_variation_list:
                # incrementa a quantidade do item
                index = exist_variation_list.index(product_list_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # cria um novo produto com variaçao diferente
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_list_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_list_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )

            if len(product_list_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_list_variation)
            cart_item.save()

        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    # SUBTRAINDO UM ITEM DO CARRINHO AO PRECIONAR O BOTAO ' - (MENOS)'

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)


        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id=None):
    # REMOVENDO UM ITEM DO CARRINHO PELO BOTÃO
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
    try:
        cart_item.delete()
    except:
        pass
    return redirect('cart')



class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'store/checkout.html'
    form_class = DeliveryAddressForm
    success_url = '/thanks/'
    
    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        total = 0
        user = self.request.user



        try:
            if self.request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(self.request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)

            freight_product = (10 * total) / 100  # calculando 10% do produto como frete_product
            grand_total = total + freight_product  # valor final do carrinho é total + frete
            context['total'] = total
            context['cart_itens'] = cart_items
            context['freight_product'] = freight_product
            context['grand_total'] = grand_total

        except ObjectDoesNotExist:
            pass

        # imprimindo endereço de entrega
        email = self.request.user
        user_account = Account.objects.get(email=email)

        try:
            context['address'] = DeliveryAddress.objects.get(user=user_account)
        except ObjectDoesNotExist:
            context['address'] = False

        #


        return context


    def form_valid(self, form):
        return super(CheckoutView, self).form_valid(form)