from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Game, Player, Tournament

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Tournament)