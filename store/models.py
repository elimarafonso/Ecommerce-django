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

    def get_url(self):
        return reverse('ProductDetail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

