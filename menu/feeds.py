from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from datetime import date
from menu.models import MenuOfTheDay

class DailyMenuFeed(Feed):
    title = _("click2eat.ro menu of the day")
    link = "/menu/feeds/"
    description = _("Menu of the day from various restaurants at click2eat.ro")

    def items(self):
        return MenuOfTheDay.objects.filter(day=date.today())

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description