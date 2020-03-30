from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/<int:game_id>', views.game, name='game'),
    path('tournaments', views.tournaments, name='tournaments'),
    path('tournament/<int:tournament_id>', views.tournament, name='tournament'),
]