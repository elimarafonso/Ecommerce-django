import decimal

from django.db import models
from store.models import Product, Variation
from accounts.models import Account


# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Itens do Carrinho'
        verbose_name_plural = 'Itens de Todos os Carrinhos'

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product


    @staticmethod
    def calcTotalCart(cart_items):
        # FUNÇÃO PARA CALCULAR O TOTAL DO CARRINHO
        total = 0
        grand_total = 0
        tax = decimal.Decimal(0.1) # FRETE
        quantity = 0
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        grand_total = (total * tax) + total
        freight_product = (10 * total) / 100  # calculando 10% do produto como frete_product
        grand_total = total + freight_product  # valor final do carrinho é total + frete
        info = {
            'freight_product': freight_product,
            'total': total,
            'quantity': quantity,
            'grand_total': grand_total
        }
        return info


