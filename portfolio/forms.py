"""
Portfolio forms - Formulaire de contact avec validation.
"""
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Formulaire de prise de contact."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Votre nom complet',
                'class': 'form-input',
                'id': 'contact-name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'votre@email.com',
                'class': 'form-input',
                'id': 'contact-email',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Sujet du message',
                'class': 'form-input',
                'id': 'contact-subject',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Décrivez votre projet ou votre demande...',
                'class': 'form-textarea',
                'rows': 6,
                'id': 'contact-message',
            }),
        }
        labels = {
            'name': 'Nom complet',
            'email': 'Email',
            'subject': 'Sujet',
            'message': 'Message',
        }
        error_messages = {
            'name': {'required': 'Veuillez saisir votre nom.'},
            'email': {'required': 'Veuillez saisir votre email.', 'invalid': 'Email invalide.'},
            'message': {'required': 'Veuillez saisir votre message.'},
        }
