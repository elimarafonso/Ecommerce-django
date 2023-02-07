from django.db import models
from django.urls import reverse
from category.models import Category


# Create your models here.


class Product(models.Model):
    product_name = models.CharField('Produto', max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField('Descrição', max_length=500, blank=True)
    price = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    images = models.ImageField('Imagem', upload_to='photo/products')
    stock = models.IntegerField('Estoque')
    is_available = models.BooleanField('Disponível ?', default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField('Criado', auto_now_add=True)
    modified_date = models.DateTimeField('Ultima Alteração', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def get_url(self):
        return reverse('ProductDetail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='cor', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='tamanho', is_active=True)


variations_category_choice = (
    ('cor', 'cor'),
    ('tamanho', 'tamanho'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField('Variação do produto', max_length=100, choices=variations_category_choice)
    variation_value = models.CharField('Valor', max_length=100)
    is_active = models.BooleanField('Ativo', default=True)
    created_date = models.DateTimeField('Data criação', auto_now_add=True)

    objects = VariationManager()

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    def __str__(self):
        return self.variation_value
