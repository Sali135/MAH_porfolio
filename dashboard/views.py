"""
Dashboard admin views — Espace administrateur personnalisé du portfolio.
Protected by @login_required, separate from Django /admin/.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from portfolio.models import Skill, Project, ContactMessage, AboutStats, TimelineItem
from .forms import (
    DashboardSkillForm, DashboardProjectForm,
    DashboardLoginForm, DashboardSignupForm,
    DashboardAboutForm, DashboardTimelineForm
)


def is_staff(user):
    return user.is_staff or user.is_superuser


def create_admin_temp(request):
    """Temporary view to create a superuser on Render Free."""
    import os
    from django.contrib.auth import get_user_model
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

    if not username or not password:
        return HttpResponse("Fermez cette page : Les variables DJANGO_SUPERUSER_USERNAME ou PASSWORD ne sont pas configurées sur Render.", status=400)

    User = get_user_model()
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()

    return HttpResponse(f"Succès ! L'utilisateur '{username}' a été {'créé' if created else 'mis à jour'}. Vous pouvez maintenant supprimer ce code.")


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def dashboard_logout(request):
    logout(request)
    messages.success(request, '✅ Déconnexion réussie.')
    return redirect('dashboard:login')


# ── AUTH ──────────────────────────────────────────────────────
def dashboard_login(request):
    """Page de connexion de l'espace admin."""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:home')

    form = DashboardLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard:home'))
        else:
            messages.error(request, '❌ Identifiants incorrects ou accès non autorisé.')

    return render(request, 'dashboard/login.html', {'form': form})


def dashboard_signup(request):
    """Page d'inscription dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
        
    form = DashboardSignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        user.is_staff = True  # Par défaut, on veut qu'ils accèdent au dashboard
        user.save()
        messages.success(request, '✅ Compte créé ! Connectez-vous maintenant.')
        return redirect('dashboard:login')
        
    return render(request, 'dashboard/signup.html', {'form': form})


# ── USERS MANAGEMENT ──────────────────────────────────────────
@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def user_list(request):
    """Liste des utilisateurs ayant accès au dashboard."""
    from django.contrib.auth.models import User
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users/list.html', {'users': users})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def user_delete(request, pk):
    """Supprimer un utilisateur."""
    from django.contrib.auth.models import User
    user_to_del = get_object_or_404(User, pk=pk)
    
    if user_to_del == request.user:
        messages.error(request, "❌ Vous ne pouvez pas vous supprimer vous-même.")
    else:
        user_to_del.delete()
        messages.success(request, f"✅ Utilisateur '{user_to_del.username}' supprimé.")
        
    return redirect('dashboard:user_list')


# ── HOME / STATS ──────────────────────────────────────────────
@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def dashboard_home(request):
    """Tableau de bord principal avec statistiques."""
    now = timezone.now()
    last_30 = now - timedelta(days=30)
    last_7 = now - timedelta(days=7)

    # Stats générales
    stats = {
        'total_projects': Project.objects.count(),
        'featured_projects': Project.objects.filter(featured=True).count(),
        'total_skills': Skill.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'messages_30d': ContactMessage.objects.filter(created_at__gte=last_30).count(),
        'messages_7d': ContactMessage.objects.filter(created_at__gte=last_7).count(),
    }

    # Projets par catégorie (pour chart)
    projects_by_category = list(
        Project.objects.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Skills par catégorie (pour chart)
    skills_by_category = list(
        Skill.objects.values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Derniers messages
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]

    # Projets récents pour la table du bas
    recent_projects = Project.objects.order_by('-created_at')[:5]

    context = {
        'stats': stats,
        'projects_by_category': projects_by_category,
        'skills_by_category': skills_by_category,
        'recent_messages': recent_messages,
        'recent_projects': recent_projects,
        # Variables globales pour la sidebar
        'total_projects': stats['total_projects'],
        'unread_count': stats['unread_messages'],
    }
    return render(request, 'dashboard/home.html', context)


# ── PROJECTS CRUD ─────────────────────────────────────────────
@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def project_list(request):
    """Liste de tous les projets avec filtres."""
    category = request.GET.get('category', '')
    search = request.GET.get('q', '')
    projects = Project.objects.prefetch_related('technologies').order_by('order', '-created_at')

    if category:
        projects = projects.filter(category=category)
    if search:
        projects = projects.filter(title__icontains=search)

    context = {
        'projects': projects,
        'category': category,
        'search': search,
        'categories': Project.CATEGORY_CHOICES,
    }
    return render(request, 'dashboard/projects/list.html', context)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def project_create(request):
    """Formulaire de création de projet."""
    form = DashboardProjectForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        project = form.save()
        messages.success(request, f'✅ Projet «{project.title}» créé avec succès !')
        return redirect('dashboard:project_list')
    return render(request, 'dashboard/projects/form.html', {'form': form, 'action': 'Créer'})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def project_edit(request, pk):
    """Formulaire d'édition de projet."""
    project = get_object_or_404(Project, pk=pk)
    form = DashboardProjectForm(request.POST or None, request.FILES or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'✅ Projet «{project.title}» mis à jour !')
        return redirect('dashboard:project_list')
    return render(request, 'dashboard/projects/form.html', {
        'form': form, 'project': project, 'action': 'Modifier'
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def project_delete(request, pk):
    """Suppression d'un projet."""
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'🗑️ Projet «{title}» supprimé.')
        return redirect('dashboard:project_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': project, 'type': 'projet', 'cancel_url': 'dashboard:project_list'
    })


# ── SKILLS CRUD ───────────────────────────────────────────────
@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def skill_list(request):
    """Liste de toutes les compétences."""
    category = request.GET.get('category', '')
    skills = Skill.objects.order_by('order', 'name')
    if category:
        skills = skills.filter(category=category)
    context = {
        'skills': skills,
        'category': category,
        'categories': Skill.CATEGORY_CHOICES,
    }
    return render(request, 'dashboard/skills/list.html', context)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def skill_create(request):
    form = DashboardSkillForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        skill = form.save()
        messages.success(request, f'✅ Compétence «{skill.name}» créée !')
        return redirect('dashboard:skill_list')
    return render(request, 'dashboard/skills/form.html', {'form': form, 'action': 'Créer'})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    form = DashboardSkillForm(request.POST or None, instance=skill)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'✅ Compétence «{skill.name}» mise à jour !')
        return redirect('dashboard:skill_list')
    return render(request, 'dashboard/skills/form.html', {
        'form': form, 'skill': skill, 'action': 'Modifier'
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        name = skill.name
        skill.delete()
        messages.success(request, f'🗑️ Compétence «{name}» supprimée.')
        return redirect('dashboard:skill_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': skill, 'type': 'compétence', 'cancel_url': 'dashboard:skill_list'
    })


# ── MESSAGES ──────────────────────────────────────────────────
@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def message_list(request):
    """Liste des messages de contact."""
    status = request.GET.get('status', '')
    msgs = ContactMessage.objects.order_by('-created_at')
    if status == 'unread':
        msgs = msgs.filter(is_read=False)
    elif status == 'read':
        msgs = msgs.filter(is_read=True)
    context = {'messages_list': msgs, 'status': status}
    return render(request, 'dashboard/messages/list.html', context)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def message_detail(request, pk):
    """Détail d'un message — marque comme lu automatiquement."""
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])
    return render(request, 'dashboard/messages/detail.html', {'msg': msg})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, '🗑️ Message supprimé.')
        return redirect('dashboard:message_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': msg, 'type': 'message', 'cancel_url': 'dashboard:message_list'
    })


# ── API AJAX ──────────────────────────────────────────────────
@login_required(login_url='dashboard:login')
def toggle_featured(request, pk):
    """Toggle le statut 'vedette' d'un projet via AJAX."""
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.featured = not project.featured
        project.save(update_fields=['featured'])
        return JsonResponse({'featured': project.featured})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required(login_url='dashboard:login')
def toggle_read(request, pk):
    """Toggle is_read d'un message via AJAX."""
    if request.method == 'POST':
        msg = get_object_or_404(ContactMessage, pk=pk)
        msg.is_read = not msg.is_read
        msg.save(update_fields=['is_read'])
        return JsonResponse({'is_read': msg.is_read})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ── À PROPOS : STATS + TIMELINE ──────────────────────────────
@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def about_edit(request):
    """Édition des stats (singleton) + liste des items timeline."""
    about = AboutStats.get_solo()
    form  = DashboardAboutForm(request.POST or None, instance=about)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Statistiques mises à jour !')
        return redirect('dashboard:about_edit')

    timeline_items = TimelineItem.objects.all()
    return render(request, 'dashboard/about/edit.html', {
        'form': form,
        'timeline_items': timeline_items,
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def timeline_create(request):
    form = DashboardTimelineForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Étape du parcours ajoutée !')
        return redirect('dashboard:about_edit')
    return render(request, 'dashboard/about/timeline_form.html', {
        'form': form, 'action': 'Ajouter'
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def timeline_edit(request, pk):
    item = get_object_or_404(TimelineItem, pk=pk)
    form = DashboardTimelineForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '✅ Étape mise à jour !')
        return redirect('dashboard:about_edit')
    return render(request, 'dashboard/about/timeline_form.html', {
        'form': form, 'item': item, 'action': 'Modifier'
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def timeline_delete(request, pk):
    item = get_object_or_404(TimelineItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, '🗑️ Étape supprimée.')
        return redirect('dashboard:about_edit')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': item, 'type': 'étape du parcours',
        'cancel_url': 'dashboard:about_edit'
    })
