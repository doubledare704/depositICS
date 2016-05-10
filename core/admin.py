from django.contrib import admin
from django.contrib.admin import site
import adminactions.actions as acts
from core.models import *


# Register your models here.


def copy_objects(modeladmin, request, queryset):
    for o in queryset:
        o.id = None
        o.save()


copy_objects.short_description = 'Copy all objects'


class CopyMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CopyMixin, self).__init__(model, admin_site)


class AllAdmin(CopyMixin, admin.ModelAdmin):
    actions = [copy_objects]


acts.add_to_site(site)
admin.site.register(SWOT, AllAdmin)
admin.site.register(Client, AllAdmin)
admin.site.register(Credits, AllAdmin)
admin.site.register(Contracts, AllAdmin)
admin.site.register(Deposits, AllAdmin)
admin.site.register(Valuta, AllAdmin)
admin.site.register(Reports, AllAdmin)
