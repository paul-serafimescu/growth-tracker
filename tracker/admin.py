from django.contrib import admin
from .models import Guild, Snapshot, DiscordUser, Graph

admin.site.register(Guild)
admin.site.register(Snapshot)
admin.site.register(DiscordUser)
admin.site.register(Graph)
