from django.urls import path

from .views import GamesList, GameDetails, TournamentsList, TournamentDetails, GameDetailsTest

urlpatterns = [
    path('', GamesList.as_view(), name='index'),
    path('game/<int:pk>', GameDetails.as_view(), name='game'),  # TODO: this will be useless after converting to dynamic page
    path('tournaments', TournamentsList.as_view(), name='tournaments'),
    path('tournament/<int:pk>', TournamentDetails.as_view(), name='tournament'),
    path('game_details/<int:pk>', GameDetailsTest.as_view(), name='game_details'),  # TODO: maybe rename to 'game' endpoint
]