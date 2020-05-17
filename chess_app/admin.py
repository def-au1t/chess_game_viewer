# Register your models here.

from django.contrib import admin
from .getdata import get_data
from .models import Game, Player, Tournament, PGN, Parse
from django.shortcuts import redirect
from django.contrib.sessions.middleware import SessionMiddleware

admin.site.register(Game)
admin.site.register(Tournament)
admin.site.register(PGN)
admin.site.register(Player)


class PgnAdd(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/parser')

    def response_change(self, request, obj):
        return redirect('/parser')

    def save_model(self, request, obj, form, change):
        obj.save()
        datas = get_data(obj.upload.path)
        pgns = datas['pgn']
        request.session['pgn'] = pgns


admin.site.register(Parse, PgnAdd)

admin.site.site_title = "Panel administracyjny"
admin.site.site_header = "Baza partii szachowych - Panel administratora"
admin.site.index_title = "Baza partii szachowych - konfiguracja"

