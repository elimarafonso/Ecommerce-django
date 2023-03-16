from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from validate_docbr import CPF
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import password_validation as validator

