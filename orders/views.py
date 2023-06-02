import datetime
import decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from accounts.models import DeliveryAddress, Account, AccessLocation
from carts.models import CartItem
from .models import Order

from django.shortcuts import redirect






# SALVAR TODAS AS INFORMAÇÕES DO PEDIDO NO BANCO DE DADOS
class PlaceOrderView(LoginRequiredMixin, TemplateView):

    template_name = 'store/orders/payments.html'

    def get_context_data(self, **kwargs):
        context = super(PlaceOrderView, self).get_context_data(**kwargs)
        current_user = self.request.user
        # verifica no template se possui itens no carrinho, caso contrario n exibe a pagina
        cart_itens = CartItem.objects.filter(user=current_user)
        context['cart_items_Exists'] = cart_itens.exists()

        email = self.request.user
        user_account = Account.objects.get(email=email)
        address = DeliveryAddress.objects.get(user=user_account)

        # total pedido
        total_order = CartItem.calcTotalCart(cart_itens)
        #

        # CRIANDO UM PEDIDO / ORDER
        pedido = Order()
        pedido.user = user_account
        pedido.order_total = total_order['grand_total']
        pedido.tax = total_order['freight_product']
        pedido.delivery_address = address
        #
        ip = self.request.META.get('REMOTE_ADDR')
        pedido.ip = AccessLocation.getIpPublic(ip)# PEGANDO IP publico. (comparar com ip de acesso do site da pra saber quem acessou e comprou)
        #
        pedido.save()

        # Gerando numero do pedido
        numberOrder = pedido.createNumber(pedido.id)
        pedido.order_number = numberOrder
        pedido.save()
        context['pedido'] = pedido
        context['total_order'] = total_order
        context['address'] = address
        context['cart_itens'] = cart_itens

        return context

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'store/orders/payments.html'
