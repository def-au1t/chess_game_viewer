from django.shortcuts import render
from django.http import HttpResponse
from chess.models import Game, Tournament, Player, PGN


def index(request):
    games = Game.objects.all()
    context = {'games': games}
    return render(request, 'index.html', context)


def game(request, game_id):
    source = request.GET.get('tid', '')
    game = Game.objects.get(id=game_id)
    context = {'game': game, 'source': source}
    return render(request, 'game.html', context)


def tournaments(request):
    tournaments_list = Tournament.objects.all()
    context = {"tournaments": tournaments_list}
    return render(request, 'tournaments.html', context)


def tournament(request, tournament_id):
    source = request.GET.get('src', '')
    tournament = Tournament.objects.get(id=tournament_id)
    games = Game.objects.filter(tournament_id=tournament.id)
    context = {"tournament": tournament, 'games': games, 'source': source}
    return render(request, 'tournament.html', context)
