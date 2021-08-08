from django.contrib import admin
from .models import Guild, Snapshot, DiscordUser

admin.site.register(Guild)
admin.site.register(Snapshot)
admin.site.register(DiscordUser)
