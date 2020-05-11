from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django_filters.views import FilterView

from .filters import TournamentsListFilter, GamesListFilter
from .getdata import get_player_data
from .models import Tournament, Game, PGN


class TournamentsList(FilterView):
    model = Tournament
    template_name = "../templates/tournament_list.html"
    paginate_by = 1  # TODO: change this later
    ordering = ['-date']

    filterset_class = TournamentsListFilter

    sel_op = {
        '': '...',
        'k': 'Klasyczne',
        's': 'Szybkie',
        'b': 'Błyskawiczne'
    }

    def get_context_data(self, **kwargs):
        return super(TournamentsList, self).get_context_data(select_options=self.sel_op, **kwargs)


class TournamentDetails(DetailView):
    model = Tournament
    template_name = "../templates/tournament.html"

    # paginate_by = 5
    # ordering = ['-id']

    def get_context_data(self, **kwargs):
        games = list(Game.objects.filter(tournament_id=self.object.id).order_by("-id"))

        games_grouped = dict()
        for game in games:
            r = game.round
            if games_grouped.get(r):
                games_grouped[r].append(game)
            else:
                games_grouped[r] = [game]
                
        context = super(TournamentDetails, self).get_context_data(object_list=sorted(games_grouped.items()), **kwargs)
        return context


class GamesList(FilterView):
    model = Game
    template_name = "../templates/game_list.html"
    paginate_by = 10
    ordering = ['id']

    filterset_class = GamesListFilter

    sel_op = {
        '': '...',
        'k': 'Klasyczne',
        's': 'Szybkie',
        'b': 'Błyskawiczne'
    }

    def get_context_data(self, **kwargs):
        return super(GamesList, self).get_context_data(select_options=self.sel_op, **kwargs)


class GameDetails(DetailView):
    model = Game
    template_name = "../templates/game.html"

    def get_context_data(self, **kwargs):
        similar_games = list(Game.objects.filter(tournament_id=self.object.tournament_id).order_by("round"))

        game_type = 'tournament'
        if len(similar_games) < 2:
            similar_games = list(Game.objects.exclude(id=self.object.id).order_by('?')[:5])
            similar_games[0] = self.object
            game_type = 'random'

        current_game_id = self.object.id
        context = super(GameDetails, self).get_context_data(
            similar_games=similar_games,
            current_game_id=current_game_id,
            type=game_type,
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
