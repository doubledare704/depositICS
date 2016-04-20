from django.contrib import admin
from django.contrib.admin import site
import adminactions.actions as actions
from core.models import *

# Register your models here.
actions.add_to_site(site)
admin.site.register(SWOT)
admin.site.register(Client)
admin.site.register(Credits)
admin.site.register(Contracts)
admin.site.register(Deposits)
admin.site.register(Valuta)
admin.site.register(Reports)
