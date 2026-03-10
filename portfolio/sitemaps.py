from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['portfolio:index']

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Project.objects.filter(featured=True)

    def lastmod(self, obj):
        return obj.updated_at
