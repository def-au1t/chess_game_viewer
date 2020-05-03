from django.urls import path
from .views import GamesList, GameDetails, TournamentsList, TournamentDetails, parse_pgn

urlpatterns = [
    path('', GamesList.as_view(), name='index'),
    path('game/<int:pk>', GameDetails.as_view(), name='game'),
    path('tournaments/', TournamentsList.as_view(), name='tournaments'),
    path('tournament/<int:pk>', TournamentDetails.as_view(), name='tournament'),
    path('parser/', parse_pgn, name='parser'),
]