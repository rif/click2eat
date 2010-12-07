from django.contrib.sitemaps import Sitemap
from restaurant.models import Unit

class UnitSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Unit.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.added_date