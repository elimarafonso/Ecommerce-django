from django.db import models

from accounts.models import Account, DeliveryAddress
from store.models import Product, Variation
from datetime import datetime

class Payment(models.Model):
    user = models.ForeignKey(Account, name='Usuário', on_delete=models.CASCADE)
    payment_method = models.CharField('Tipo do Pagamento', max_length=100)
    amount_paid = models.CharField('Valor Pago', max_length=100) # valor total pago
    status = models.CharField('Status', max_length=100)
    created_at = models.DateTimeField('Data de Pagamento', auto_now_add=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'


    def __str__(self):
        return self.payment_id

class Order(models.Model):

    STATUS = (
        ('New', 'Novo'),
        ('Accepted', 'Aceito'),
        ('Completed', 'Concluído'),
        ('Cancelled', 'Cancelado'),
    )

    user = models.ForeignKey(Account,  on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment,  on_delete=models.SET_NULL, blank=True, null=True)
    delivery_address = models.ForeignKey(DeliveryAddress,  on_delete=models.CASCADE, null=False, blank=False)
    order_number = models.CharField('Número do Pedido', max_length=20)
    order_total = models.DecimalField('Total do pedido',  max_digits=8, decimal_places=2)
    tax = models.DecimalField('Taxa',  max_digits=8, decimal_places=2)
    status = models.CharField('Status', max_length=10, choices=STATUS, default='Novo')
    # dados do ip de compra
    ip = models.CharField('IP', blank=True, max_length=20)
    #
    is_ordered = models.BooleanField('Ordenado', default=True)
    created_at = models.DateTimeField('Data de criação', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Pedido de compra'
        verbose_name_plural = 'Pedidos de compras'

    def __str__(self):
        return self.order_number

    def createNumber(self, id):
        date = datetime.today()
        d = datetime.date(date)
        number = d.strftime('%d%m%Y') + str(id) # Dia + Mes + Ano + IDdopedido ->
        return number


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, name='Pedido', on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, name='Pagamento', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, name='Usuário', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, name='Produto', on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, name='Variação', on_delete=models.CASCADE)
    # VERIFICAR SE É NECESSÁRIO ESTES DOIS CAMPOS, PORQUE A VARIAÇÃO DO PRODUTO JA
    # TRÁS AS CARACTERISTICAS DO PRODUTO CADASTRADO
    # color = models.CharField(max_length=50)
    # size = models.CharField(max_length=50)
    #
    #
    quantity = models.IntegerField()
    product_price = models.FloatField('Valor do produto')
    ordered = models.BooleanField('Ordenado', default=False)
    created_at = models.DateTimeField('Adicionado', auto_now_add=True)
    updated_at = models.DateTimeField('Alterado', auto_now=True)

    class Meta:
        verbose_name = 'Produto do pedido'
        verbose_name_plural = 'Produtos do pedido'

    def __str__(self):
        return self.product.product_name




