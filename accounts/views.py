from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import RegistrationForm, Account
from django.contrib import messages


class RegisterFormView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('register')


    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        docCPF = form.cleaned_data['docCPF']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']

        password = form.cleaned_data['password']
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, docCPF=docCPF,
                                           email=email, password=password)
        user.phone_number = phone_number
        user.save()

        messages.success(self.request, f'Seja bem vindo, {first_name}!')

        return super().form_valid(form)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class LogoutView(TemplateView):
    template_name = 'accounts/logout.html'
