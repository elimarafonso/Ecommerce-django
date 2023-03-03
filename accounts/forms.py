from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Account

from validate_docbr import CPF
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import password_validation as validator

'''
FORMULÁRIO DE CRIÇÃO/EDIÇÃO DE USUÁRIOS!
'''


class AccountCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'phone_number')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'phone_number')


#####################################
#                                   #
# REGISTRO DE USUÁRIOS DO SITE      #
#                                   #
#####################################


class RegistrationForm(forms.ModelForm):
    # registro de usuarios
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Digite uma senha',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme a senha',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'docCPF', 'email', 'phone_number', 'password']

    def clean_docCPF(self):
        doc = self.cleaned_data['docCPF']
        if self.valida_doc(doc):
            return doc
        else:
            raise ValidationError('CPF inválido.')

    def valida_doc(self, doc):
        cpf = CPF()
        # Não aceitando entradas de 000.000.000-00/ 111.111.111-11 / 222.222.222-22 até 999.999.999-99
        cpf.repeated_digits = False
        doc = str(doc)
        return cpf.validate(doc)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        validator.validate_password(password)

        if password != confirm_password:
            raise forms.ValidationError(
                'As senhas NÃO são iguais, por favor confirme novamente'
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Digite seu primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Digite seu segundo nome'
        self.fields['docCPF'].widget.attrs['placeholder'] = '___.___.___-__'
        self.fields['phone_number'].widget.attrs['placeholder'] = '(DDD) X XXXX-XXXX'
        self.fields['password'].widget.attrs['placeholder'] = 'Digite sua senha'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Digite uma senha'
    }))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.PasswordInput(attrs={
        'placeholder': 'seu email'
    }))

    class Meta:
        model = Account
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            user = Account.objects.get(email__exact=email)
            return user
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                'E-mail não encontrado!'
            )

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Digite uma senha',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme a senha',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['password']

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        validator.validate_password(password)

        if password != confirm_password:
            raise forms.ValidationError(
                'As senhas NÃO são iguais, por favor confirme novamente'
            )

