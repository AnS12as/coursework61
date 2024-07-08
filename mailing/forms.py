from django import forms
from .models import Mailing, Client, Message
from django.forms.widgets import DateTimeInput


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_datetime', 'periodicity', 'status', 'message', 'clients']
        widgets = {
            'start_datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
