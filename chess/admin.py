# Register your models here.

from django.contrib import admin

from .models import Game, Player, Tournament, PGN

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(PGN)