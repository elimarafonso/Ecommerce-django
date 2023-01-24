from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account

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
