"""
Portfolio admin - Interface d'administration personnalisée.
"""
from django.contrib import admin
from django.utils.html import mark_safe
from .models import Skill, Project, ContactMessage


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency_bar', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('order', 'name')

    def proficiency_bar(self, obj):
        color = obj.color or '#3b82f6'
        return mark_safe(
            f'<div style="width:120px;background:#e2e8f0;border-radius:4px;height:8px;">'
            f'<div style="width:{obj.proficiency}%;background:{color};height:8px;border-radius:4px;"></div>'
            f'</div> {obj.proficiency}%'
        )
    proficiency_bar.short_description = 'Niveau'


class ProjectTechInline(admin.TabularInline):
    model = Project.technologies.through
    extra = 1
    verbose_name = 'Technologie'
    verbose_name_plural = 'Technologies'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'order', 'created_at', 'preview_image')
    list_editable = ('featured', 'order')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'preview_image_large')
    inlines = [ProjectTechInline]
    exclude = ('technologies',)

    fieldsets = (
        ('Infos principales', {
            'fields': ('title', 'slug', 'category', 'featured', 'order')
        }),
        ('Contenu', {
            'fields': ('description', 'problem', 'solution', 'impact')
        }),
        ('Médias & Liens', {
            'fields': ('image', 'preview_image_large', 'github_url', 'demo_url')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height:40px;border-radius:4px;" />'
            )
        return '—'
    preview_image.short_description = 'Aperçu'

    def preview_image_large(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height:200px;border-radius:8px;" />'
            )
        return '—'
    preview_image_large.short_description = 'Aperçu image'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


# Personnalisation de l'interface admin
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio"
admin.site.index_title = "Gestion du Portfolio"
