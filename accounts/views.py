from smtplib import SMTPException

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .forms import RegistrationForm, Account, LoginForm, ForgotPasswordForm, ResetPasswordForm
from django.contrib import messages
from django.contrib import auth
from accounts.forms import DeliveryAddressForm
from .models import Account, DeliveryAddress

# VERIFICAÇÃO DE EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def validate_and_sendEmail(self, subject, user, email, url):
    try:
        current_site = get_current_site(self.request)
        mail_subject = f'Capelinha Store, {subject}'
        message = render_to_string(f'{url}', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    except SMTPException as e:
        messages.error(self.request, f'Erro <{e}>')


def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        request.session['email'] = user.email
        messages.success(request, "Por favor crie uma nova senha")
        return redirect('resetPassword')
    else:
        messages.error(request, f'Link inválido!')
        return redirect('login')


class ForgotPasswordView(FormView):
    template_name = 'accounts/forgotPassword.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # retorna um objecto pq sobrescrevi o metodo cleaned_data em forms no metodo clean_email
        user = form.cleaned_data['email']

        # verificando e enviando e-mail
        subject = 'ative sua conta!'
        url = 'accounts/resetPassword_email.html'
        validate_and_sendEmail(self, subject=subject, user=user, email=user.email, url=url)
        #
        messages.success(self.request, 'Enviamos um e-mail para redefinir sua senha!')

        return super().form_valid(form)


class ResetPasswordFormView(FormView):
    template_name = 'accounts/resetPasswordForm.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('login')

    def render_to_response(self, context, **response_kwargs):
        context['email'] = self.request.session['email']

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def form_invalid(self, form):

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        password = form.cleaned_data['password']

        try:
            id = self.request.session['uid']
            user = Account.objects.get(id=id)
            user.set_password(password)

            user.save()
            messages.success(self.request, 'senha alterada!')

        except Exception as e:
            messages.error(self.request, f'Erro: {e}')
        return super().form_valid(form)


class RegisterFormView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = 'home'

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name'].strip()
        last_name = form.cleaned_data['last_name'].strip()
        docCPF = form.cleaned_data['docCPF']
        email = form.cleaned_data['email'].strip()
        phone_number = form.cleaned_data['phone_number'].strip()
        password = form.cleaned_data['password']

        user = Account.objects.create_user(first_name=first_name, last_name=last_name, docCPF=docCPF,
                                           email=email, password=password)
        user.phone_number = phone_number
        user.save()

        # verificando e enviando e-mail
        subject = 'ative sua conta!'
        url = 'accounts/accounts_verification_email.html'
        validate_and_sendEmail(self, subject=subject, user=user, email=email, url=url)
        #

        self.success_url = reverse_lazy('login') + f'?command=verification&email={email}'
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = auth.authenticate(self, username=email, password=password)

        if user is not None:
            auth.login(self.request, user)
            messages.success(self.request, f'Seja bem vindo, {user.first_name} ')
        else:
            messages.error(self.request, "E-mail ou senha não compativeis !")
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, RedirectView, FormView):
    pattern_name = 'login'
    form_class = LoginForm

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            auth.logout(self.request)
            messages.success(self.request, "Você saiu do sistema")

        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


def Activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # {user.first_name}
        messages.success(request, f'Olá {user.first_name.capitalize()}, seu E-mail foi validado com sucesso!!!')
        return redirect('login')
    else:
        messages.error(request, f'Link de ativação inválido!')
        return redirect('register')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard/overview.html'


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/dashboard/updateAddress.html'
    form_class = DeliveryAddressForm
    model = DeliveryAddress
    success_url = reverse_lazy('listAddress')

    def form_valid(self, form):
        messages.success(self.request, "Endereço Alterado !")
        return super(UpdateAddressView, self).form_valid(form)


class CreateAddressView(LoginRequiredMixin, FormView):
    template_name = 'accounts/dashboard/registerAddress.html'
    form_class = DeliveryAddressForm
    success_url = reverse_lazy('listAddress')

    def form_valid(self, form):

        email = form.cleaned_data['user']
        fullName = form.cleaned_data['fullName']
        phoneNumber = form.cleaned_data['phoneNumber']
        docCPF = form.cleaned_data['docCPF']
        cep = form.cleaned_data['cep']
        state = form.cleaned_data['state']
        city = form.cleaned_data['city']
        district = form.cleaned_data['district']
        street = form.cleaned_data['street']
        number = form.cleaned_data['number']
        complement = form.cleaned_data['complement']
        observation = form.cleaned_data['observation']

        try:
            user = Account.objects.get(email=email)

            newAddress = DeliveryAddress(user=user,
                                         fullName=fullName,
                                         phoneNumber=phoneNumber,
                                         docCPF=docCPF,
                                         cep=cep,
                                         state=state,
                                         city=city,
                                         district=district,
                                         street=street,
                                         number=number,
                                         complement=complement,
                                         observation=observation
                                         )
            newAddress.save()
            messages.success(self.request, "Endereço Salvo")

        except ObjectDoesNotExist:
            messages.error(self.request, "O sistema encontrou dois endereços para esse usuario")


        return super(CreateAddressView, self).form_valid(form)

class ListAddressView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard/listAddress.html'

    def get_context_data(self, **kwargs):
        context = super(ListAddressView, self).get_context_data(**kwargs)
        email = self.request.user
        user_account = Account.objects.get(email=email)

        try:
            context['address'] = DeliveryAddress.objects.get(user=user_account)
        except ObjectDoesNotExist:
            context['address'] = False
        return context


class DeleteAddressView(DeleteView):
    pass