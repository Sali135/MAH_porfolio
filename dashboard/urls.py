"""
Dashboard app URLs.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Auth
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    path('inscription/', views.dashboard_signup, name='signup'),
    path('create-admin-xyz-99/', views.create_admin_temp),

    # Users
    path('utilisateurs/', views.user_list, name='user_list'),
    path('utilisateurs/<int:pk>/supprimer/', views.user_delete, name='user_delete'),

    # Home
    path('', views.dashboard_home, name='home'),

    # Projects
    path('projets/', views.project_list, name='project_list'),
    path('projets/nouveau/', views.project_create, name='project_create'),
    path('projets/<int:pk>/modifier/', views.project_edit, name='project_edit'),
    path('projets/<int:pk>/supprimer/', views.project_delete, name='project_delete'),

    # Skills
    path('competences/', views.skill_list, name='skill_list'),
    path('competences/nouvelle/', views.skill_create, name='skill_create'),
    path('competences/<int:pk>/modifier/', views.skill_edit, name='skill_edit'),
    path('competences/<int:pk>/supprimer/', views.skill_delete, name='skill_delete'),

    # Messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/supprimer/', views.message_delete, name='message_delete'),

    # AJAX
    path('api/projet/<int:pk>/featured/', views.toggle_featured, name='toggle_featured'),
    path('api/message/<int:pk>/read/', views.toggle_read, name='toggle_read'),

    # À Propos
    path('apropos/',                         views.about_edit,      name='about_edit'),
    path('apropos/timeline/ajouter/',        views.timeline_create, name='timeline_create'),
    path('apropos/timeline/<int:pk>/modifier/', views.timeline_edit, name='timeline_edit'),
    path('apropos/timeline/<int:pk>/supprimer/', views.timeline_delete, name='timeline_delete'),
]
