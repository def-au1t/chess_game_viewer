from django.urls import path

from .views import GamesList, GameDetails, TournamentsList, TournamentDetails

urlpatterns = [
    path('', GamesList.as_view(), name='index'),
    path('game/<int:pk>', GameDetails.as_view(), name='game'),
    path('tournaments/', TournamentsList.as_view(), name='tournaments'),
    path('tournament/<int:pk>', TournamentDetails.as_view(), name='tournament'),
]