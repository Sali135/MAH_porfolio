"""
Portfolio views - Class-Based Views pour le portfolio.
"""
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Skill, Project, ContactMessage, AboutStats, TimelineItem
from .forms import ContactForm


class IndexView(TemplateView):
    """Vue principale - Single-page portfolio."""
    template_name = 'portfolio/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Skills groupés par catégorie
        context['skills'] = Skill.objects.all()
        context['backend_skills'] = Skill.objects.filter(category='backend').order_by('order')
        context['frontend_skills'] = Skill.objects.filter(category='frontend').order_by('order')
        context['database_skills'] = Skill.objects.filter(category='database').order_by('order')
        context['devops_skills'] = Skill.objects.filter(category='devops').order_by('order')
        context['mobile_skills'] = Skill.objects.filter(category='mobile').order_by('order')

        # Projets (vedettes en premier, puis tous)
        context['featured_projects'] = Project.objects.filter(featured=True).order_by('order')
        context['all_projects'] = Project.objects.all().order_by('order')

        # Formulaire de contact
        context['contact_form'] = ContactForm()

        # Stats depuis la base de données (singleton)
        about = AboutStats.get_solo()
        context['stats'] = {
            'years_exp':     about.years_exp,
            'projects_done': about.projects_done,
            'clients':       about.clients,
            'coffee':        about.coffee,
        }

        # Timeline du parcours
        context['timeline_items'] = TimelineItem.objects.all()

        return context


    def post(self, request, *args, **kwargs):
        """Traitement du formulaire de contact."""
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Notification email (si configuré)
            try:
                send_mail(
                    subject=f"[Portfolio] Nouveau message de {contact.name}",
                    message=f"De: {contact.name} <{contact.email}>\n\n{contact.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER or 'votre@email.com'],
                    fail_silently=True,
                )
            except Exception:
                pass  # En mode dev, email s'affiche dans la console

            messages.success(
                request,
                '✅ Message envoyé avec succès ! Je vous répondrai dans les 24h.'
            )
            return redirect('portfolio:index')
        else:
            messages.error(
                request,
                '❌ Erreur dans le formulaire. Veuillez vérifier vos informations.'
            )
            context = self.get_context_data()
            context['contact_form'] = form
            return render(request, self.template_name, context)


# Error handlers
def error_404(request, exception):
    return render(request, 'portfolio/404.html', status=404)


def error_500(request):
    return render(request, 'portfolio/500.html', status=500)
