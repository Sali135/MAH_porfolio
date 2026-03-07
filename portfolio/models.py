"""
Portfolio app - Models
Skill, Project, ContactMessage avec best practices Django 5.1
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    """Compétence technique avec niveau de maîtrise."""

    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Base de données'),
        ('devops', 'DevOps'),
        ('mobile', 'Mobile'),
        ('other', 'Autre'),
    ]

    name = models.CharField(_('Nom'), max_length=50)
    category = models.CharField(
        _('Catégorie'), max_length=20,
        choices=CATEGORY_CHOICES, default='backend'
    )
    proficiency = models.IntegerField(
        _('Niveau (%)'),
        help_text='Valeur entre 0 et 100'
    )
    icon = models.CharField(
        _('Icône (classe CSS/SVG name)'),
        max_length=100,
        blank=True,
        help_text='Ex: devicon-django-plain, devicon-python-plain'
    )
    color = models.CharField(
        _('Couleur accent'),
        max_length=7,
        default='#3b82f6',
        help_text='Code HEX, ex: #3b82f6'
    )
    order = models.PositiveIntegerField(_('Ordre d\'affichage'), default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _('Compétence')
        verbose_name_plural = _('Compétences')

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"


class Project(models.Model):
    """Projet dans le portfolio."""

    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('fullstack', 'Fullstack'),
        ('mobile', 'Mobile'),
        ('api', 'API / Microservice'),
    ]

    title = models.CharField(_('Titre'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True, max_length=120)
    description = models.TextField(_('Description'))
    problem = models.TextField(_('Problème résolu'), blank=True)
    solution = models.TextField(_('Solution apportée'), blank=True)
    impact = models.TextField(_('Impact / Résultats'), blank=True)
    image = models.ImageField(
        _('Image'), upload_to='projects/', blank=True, null=True
    )
    category = models.CharField(
        _('Catégorie'), max_length=20,
        choices=CATEGORY_CHOICES, default='fullstack'
    )
    technologies = models.ManyToManyField(
        Skill, verbose_name=_('Technologies'), blank=True
    )
    github_url = models.URLField(_('Lien GitHub'), blank=True)
    demo_url = models.URLField(_('Lien Démo'), blank=True)
    featured = models.BooleanField(_('Projet vedette'), default=False)
    order = models.PositiveIntegerField(_('Ordre'), default=0)
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modifié le'), auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('Projet')
        verbose_name_plural = _('Projets')

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return self.technologies.all()


class ContactMessage(models.Model):
    """Message reçu via le formulaire de contact."""

    name = models.CharField(_('Nom'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Sujet'), max_length=200, blank=True)
    message = models.TextField(_('Message'))
    is_read = models.BooleanField(_('Lu'), default=False)
    created_at = models.DateTimeField(_('Reçu le'), auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Message de contact')
        verbose_name_plural = _('Messages de contact')

    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%d/%m/%Y')})"


class AboutStats(models.Model):
    """Singleton — chiffres de la section À propos."""
    years_exp      = models.PositiveIntegerField(_("Années d'expérience"), default=3)
    projects_done  = models.PositiveIntegerField(_("Projets livrés"),      default=10)
    clients        = models.PositiveIntegerField(_("Clients satisfaits"),   default=8)
    coffee         = models.PositiveIntegerField(_("Cafés ☕"),             default=500)

    class Meta:
        verbose_name = _("Statistiques À propos")

    def __str__(self):
        return "Statistiques À propos"

    @classmethod
    def get_solo(cls):
        """Retourne l'unique instance, la crée si elle n'existe pas."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class TimelineItem(models.Model):
    """Élément du parcours professionnel affiché dans la timeline."""
    period      = models.CharField(_("Période"), max_length=50,
                                   help_text="Ex : 2022 – 2024")
    title       = models.CharField(_("Titre du poste"), max_length=120)
    description = models.CharField(_("Description courte"), max_length=250)
    order       = models.PositiveIntegerField(_("Ordre d'affichage"), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _("Élément Timeline")
        verbose_name_plural = _("Éléments Timeline")

    def __str__(self):
        return f"{self.period} — {self.title}"
