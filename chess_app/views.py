from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.forms import modelformset_factory
from .models import Tournament, Game, PGN
from .forms import PgnForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sessions.middleware import SessionMiddleware
from .getdata import get_player_data


class TournamentsList(ListView):
    model = Tournament
    template_name = "../templates/tournaments.html"
    paginate_by = 5
    ordering = ['-date']


class TournamentDetails(DetailView, MultipleObjectMixin):
    model = Tournament
    template_name = "../templates/tournament.html"
    # paginate_by = 5
    # ordering = ['-id']

    def get_context_data(self, **kwargs):
        games = list(Game.objects.filter(tournament_id=self.object.id).order_by("-id"))
        rounds = set()
        for game in games:
            rounds.add(game.round)

        games_grouped = dict()
        for single_round in rounds:
            games_grouped[single_round] = [game for game in games if game.round == single_round]
        context = super(TournamentDetails, self).get_context_data(object_list=games_grouped.items(), **kwargs)
        return context

class GamesList(ListView):
    model = Game
    template_name = "../templates/index.html"
    paginate_by = 10
    ordering = ['id']


class GameDetails(DetailView):
    model = Game
    template_name = "../templates/game.html"

    def get_context_data(self, **kwargs):
        similar_games = list(Game.objects.filter(tournament_id=self.object.tournament_id).order_by("round"))
        type='tournament'
        if len(similar_games) < 2:
            similar_games = list(Game.objects.exclude(id=self.object.id).order_by('?')[:5])
            similar_games[0] = self.object
            type='random'
        current_game_id = self.object.id
        context = super(GameDetails, self).get_context_data(
            similar_games=similar_games,
            current_game_id=current_game_id,
            type=type,
            **kwargs)
        return context



@user_passes_test(lambda u: u.is_superuser)
def parse_pgn(request):
    pgns = request.session.get('pgn')
    PgnFormSet = modelformset_factory(PGN, fields=('pgn',), extra=len(pgns))

    if request.method == 'POST':
        formset = PgnFormSet(request.POST)

        if formset.is_valid():
            for f in formset:
                cd = f.cleaned_data
                data = cd.get('pgn')
                get_player_data(data)
            formset.save()
            request.session['pgn'] = ""
            return redirect('/admin/chess_app/pgn')

        return render(request, 'parser.html', {'formset': formset})
    else:
        formset = PgnFormSet(queryset=PGN.objects.none(), initial=[{'pgn': x} for x in pgns])
        return render(request, 'parser.html', {'formset': formset})

