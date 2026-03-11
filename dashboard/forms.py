"""
Dashboard forms — Formulaires personnalisés pour l'espace admin.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from portfolio.models import Skill, Project, AboutStats, TimelineItem


class DashboardLoginForm(forms.Form):
    """Formulaire de connexion dashboard."""
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={
            'placeholder': 'admin',
            'class': 'dash-input',
            'id': 'login-username',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'dash-input',
            'id': 'login-password',
            'autocomplete': 'current-password',
        })
    )
class DashboardSignupForm(UserCreationForm):
    """Formulaire d'inscription dashboard."""
    email = forms.EmailField(
        label='Adresse mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'votre@email.com',
            'class': 'dash-input',
            'id': 'signup-email',
        })
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'admin',
                'class': 'dash-input',
                'id': 'signup-username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # S'assurer que les champs mot de passe ont la bonne classe
        self.fields['password1'].widget.attrs.update({
            'class': 'dash-input',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'dash-input',
            'placeholder': 'Confirmer le mot de passe'
        })

class DashboardSkillForm(forms.ModelForm):
    """Formulaire compétence."""

    class Meta:
        model = Skill
        fields = ['name', 'category', 'proficiency', 'icon', 'color', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'dash-input', 'placeholder': 'Django, Python...'
            }),
            'category': forms.Select(attrs={'class': 'dash-input'}),
            'proficiency': forms.NumberInput(attrs={
                'class': 'dash-input', 'min': 0, 'max': 100,
                'placeholder': '85'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'devicon-django-plain'
            }),
            'color': forms.TextInput(attrs={
                'class': 'dash-input dash-color',
                'type': 'color',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'dash-input', 'min': 0, 'placeholder': '0'
            }),
        }
        labels = {
            'name': 'Nom de la compétence',
            'category': 'Catégorie',
            'proficiency': 'Niveau (%)',
            'icon': 'Classe Devicon',
            'color': 'Couleur accent',
            'order': 'Ordre d\'affichage',
        }


class DashboardProjectForm(forms.ModelForm):
    """Formulaire projet."""

    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'category', 'featured', 'order',
            'description', 'problem', 'solution', 'impact',
            'image', 'github_url', 'demo_url', 'technologies',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'dash-input', 'placeholder': 'Titre du projet'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'dash-input', 'placeholder': 'url-du-projet'
            }),
            'category': forms.Select(attrs={'class': 'dash-input'}),
            'featured': forms.CheckboxInput(attrs={'class': 'dash-checkbox'}),
            'order': forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
            'description': forms.Textarea(attrs={
                'class': 'dash-input dash-textarea',
                'rows': 4, 'placeholder': 'Description générale du projet...'
            }),
            'problem': forms.Textarea(attrs={
                'class': 'dash-input dash-textarea',
                'rows': 3, 'placeholder': 'Quel problème ce projet résout-il ?'
            }),
            'solution': forms.Textarea(attrs={
                'class': 'dash-input dash-textarea',
                'rows': 3, 'placeholder': 'Comment avez-vous résolu ce problème ?'
            }),
            'impact': forms.Textarea(attrs={
                'class': 'dash-input dash-textarea',
                'rows': 3, 'placeholder': 'Quel est l\'impact ou les résultats ?'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'dash-file-input'}),
            'github_url': forms.URLInput(attrs={
                'class': 'dash-input', 'placeholder': 'https://github.com/...'
            }),
            'demo_url': forms.URLInput(attrs={
                'class': 'dash-input', 'placeholder': 'https://demo.example.com'
            }),
            'technologies': forms.CheckboxSelectMultiple(attrs={'class': 'dash-checkboxes'}),
        }
        labels = {
            'title': 'Titre',
            'slug': 'Slug URL',
            'category': 'Catégorie',
            'featured': 'Projet vedette ⭐',
            'order': 'Ordre',
            'description': 'Description',
            'problem': 'Problème résolu',
            'solution': 'Solution apportée',
            'impact': 'Impact & Résultats',
            'image': 'Image du projet',
            'github_url': 'Lien GitHub',
            'demo_url': 'Lien Démo',
            'technologies': 'Technologies utilisées',
        }


class DashboardAboutForm(forms.ModelForm):
    """Formulaire pour les statistiques de la section À propos."""
    class Meta:
        model = AboutStats
        fields = ['years_exp', 'projects_done', 'clients', 'coffee']
        widgets = {
            'years_exp':     forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
            'projects_done': forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
            'clients':       forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
            'coffee':        forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
        }
        labels = {
            'years_exp':     "Années d'expérience",
            'projects_done': 'Projets livrés',
            'clients':       'Clients satisfaits',
            'coffee':        'Cafés ☕',
        }


class DashboardTimelineForm(forms.ModelForm):
    """Formulaire pour les éléments du parcours timeline."""
    class Meta:
        model = TimelineItem
        fields = ['period', 'title', 'description', 'order']
        widgets = {
            'period':      forms.TextInput(attrs={'class': 'dash-input', 'placeholder': '2024 – Présent'}),
            'title':       forms.TextInput(attrs={'class': 'dash-input', 'placeholder': 'Développeur Freelance'}),
            'description': forms.TextInput(attrs={'class': 'dash-input', 'placeholder': 'Django · APIs · ...'}),
            'order':       forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
        }
        labels = {
            'period':      'Période',
            'title':       'Titre du poste',
            'description': 'Description courte',
            'order':       "Ordre d'affichage",
        }
