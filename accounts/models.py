from django.db import models

'''
######################################################################
VERIFICAR SE É ASSIM QUE SE CRIA UMA AUTENTICAÇAO DE USUÁRIO 
MUDA A MANEIRA DE LOGAR NA AREA ADMINISTRATIVA
######################################################################
'''

from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Todo usuário precisa ter um E-mail')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,  email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email,  password, **extra_fields)

    def create_superuser(self,  email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ser is_superuser = True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ser is_staff = True')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractUser):
    first_name = models.CharField('Primeiro Nome', max_length=50)
    last_name = models.CharField('Segundo Nome', max_length=50)
    docCPF = models.IntegerField('CPF', unique=True)
    docCNPJ = models.IntegerField('CNPJ', default=0)
    email = models.EmailField('E-mail', max_length=100, unique=True)
    phone_number = models.CharField('Telefone:', max_length=15)
    is_staff = models.BooleanField('Pode acessar a Administração?', default=True)
    # filtros necessários do Django

    USERNAME_FIELD = 'email'
    # caso queira mais atributos é só adicionar o campo e aqui
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'docCPF']

    def __str__(self):
        return self.email

    objects = MyAccountManager()


class DeliveryAddress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=150, blank=False)
    phoneNumber = models.CharField(max_length=15, blank=False)
    docCPF = models.CharField(max_length=11, blank=False)
    cep = models.CharField(max_length=250, blank=False)
    state = models.CharField(max_length=2, blank=False)
    city = models.CharField(max_length=100, blank=False)
    district = models.CharField(max_length=100, blank=False)
    street = models.CharField(max_length=100, blank=False)
    complement = models.CharField(max_length=100, blank=False)
    number = models.IntegerField()
    observation = models.CharField(max_length=500,  blank=True)
    modified_date = models.DateTimeField(auto_now=True)





