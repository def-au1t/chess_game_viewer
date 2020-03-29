from django.shortcuts import render
from django.http import HttpResponse
from chess.models import Game, Tournament, Player


# Create your views here.

def index(request):
    games = Game.objects.all()
    players = Player.objects.all()
    for game in games:
        game.white_name = players.get(id=game.white_player_id_id).first_name\
                          + " " + players.get(id=game.white_player_id_id).last_name
        game.black_name = players.get(id=game.black_player_id_id).first_name\
                          + " " + players.get(id=game.black_player_id_id).last_name
    context = {'games': games, 'players': players}
    return render(request, 'index.html', context);


def tournaments(request):
    return HttpResponse("Hello, world. You're at tournaments index.")


def tournament(request, tournament_id):
    return HttpResponse("Hello, world. You're at tournament number %s." % tournament_id)
