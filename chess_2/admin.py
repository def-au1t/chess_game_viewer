# Register your models here.

from django.contrib import admin
from .getdata import get_player_data
from .models import Game, Player, Tournament, PGN, Parse
from django.shortcuts import redirect

admin.site.register(Game)

admin.site.register(Tournament)

pgn = ""


class MyModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(MyModelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['pgn'].initial = pgn
        return form

    def save_model(self, request, obj, form, change):
        obj.save()
        global pgn
        pgn = ""


class PgnAdd(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/chess_2/pgn/add')

    def response_change(self, request, obj):
        return redirect('/admin/chess_2/pgn/add')

    def save_model(self, request, obj, form, change):
        obj.save()
        datas = get_player_data(obj.upload.path)
        global pgn
        pgn = datas['pgn']


admin.site.register(PGN, MyModelAdmin)
admin.site.register(Player)
admin.site.register(Parse, PgnAdd)
