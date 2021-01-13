from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from karting_track_system.models import *

models = [Client, Kart, KartModel, Track, Race, RaceDrivers, Lap]
for m in models:
    admin.site.register(m)

class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Clients'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ClientInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)