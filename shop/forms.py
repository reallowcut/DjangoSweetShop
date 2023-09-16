from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class OrderForm(forms.Form):
    number = PhoneNumberField(label='Ваш телефон', widget=forms.NumberInput({
                                           'class': 'form-control'
                                       }))

    delivery_address = forms.CharField(label='Адрес доставки', max_length=100,
                                       widget=forms.TextInput({
                                           'class': 'form-control'
                                       }))
    order_comment = forms.CharField(label='Комментарий к заказу', widget=forms.Textarea({
        'class': 'form-control'
    }))

    birthday = forms.DateField(label='Дата доставки', required=True,
                               widget=MyDateInput({
                                   'class': 'form-control'
                               }))
