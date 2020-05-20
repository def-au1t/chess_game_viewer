from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django_filters.views import FilterView
from .forms import TournamentForm
from .filters import TournamentsListFilter, GamesListFilter
from .getdata import parse_data, get_tournament_data
from .models import Tournament, Game, PGN
from dateutil.parser import parse
from django.db.models import F


class TournamentsList(FilterView):
    model = Tournament
    template_name = "../templates/tournament_list.html"
    paginate_by = 10
    ordering = [F('date').desc(nulls_last=True), '-id']

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
            if r is None:
                r = 0
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
    ordering = ['-id']

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

        similar_random = False
        similar_games = []

        if self.object.tournament_id:
            similar_games = list(Game.objects.filter(tournament_id=self.object.tournament_id).order_by("round"))

        if not self.object.tournament_id or len(similar_games) < 2:
            similar_games = list(Game.objects.exclude(id=self.object.id).order_by('?')[:5])
            if(len(similar_games)) > 0:
                similar_games[0] = self.object
            similar_random = True

        current_game_id = self.object.id
        context = super(GameDetails, self).get_context_data(
            similar_games=similar_games,
            current_game_id=current_game_id,
            similar_random=similar_random,
            **kwargs)
        return context


@login_required(login_url='/admin/login/')
def parse_pgn(request):
    pgns = request.session.get('pgn')
    PgnFormSet = modelformset_factory(PGN, fields=('pgn',), extra=len(pgns))
    t_name = request.session.get("t_name")
    tmp_tournament, created = Tournament.objects.get_or_create(name=t_name)

    if not created:
        description = tmp_tournament.description
        time = tmp_tournament.time
        time_add = tmp_tournament.time_add
        type = tmp_tournament.type
        link = tmp_tournament.link
    else:
        description = ""
        time = 0
        time_add = 0
        type = ""
        link = ""

    if t_name == "?":
        t_name = None

    t_date_str = request.session.get("t_date")
    t_city = request.session.get("t_city")

    if t_city == "?":
        t_city = None

    try:
        t_date = parse(t_date_str).date()
        if t_date.year < 1950:
            t_date = None
    except ValueError:
        t_date = None

    if request.method == 'POST':
        t_form = TournamentForm(request.POST)
        formset = PgnFormSet(request.POST)
        if formset.is_valid() and t_form.is_valid():
            t_cd = t_form.cleaned_data
            tournament = get_tournament_data(t_cd)
            for f in formset:
                cd = f.cleaned_data
                if not cd:
                    continue

                data = cd.get('pgn')
                parse_data(data, tournament)

            request.session['pgn'] = ""
            request.session['t_name'] = ""
            request.session['t_date'] = ""
            request.session['city'] = ""
            return redirect('/admin/chess_app/pgn')

        return render(request, 'parser.html', {'t_form': t_form, 'formset': formset})
    else:
        t_form = TournamentForm(initial={'name': t_name, 'date': t_date, 'city': t_city, 'description': description,
                                         'time': time, 'time_add': time_add, 'type': type, 'link': link})
        formset = PgnFormSet(queryset=PGN.objects.none(), initial=[{'pgn': x} for x in pgns])
        return render(request, 'parser.html', {'t_form': t_form, 'formset': formset})


def download_pgn(request, pgn_id):
    file = PGN.objects.get(id=pgn_id).pgn
    response = HttpResponse(file, content_type='application/text')
    response['Content-Disposition'] = 'attachment; filename="game.pgn"'
    return response


