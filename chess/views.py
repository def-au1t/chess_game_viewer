from django.views.generic import ListView, DetailView
from chess.models import Tournament, Game
from django.views.generic.list import MultipleObjectMixin
from django.core import serializers
from django.http import JsonResponse

class TournamentsList(ListView):
    model = Tournament
    template_name = "../templates/tournaments.html"
    paginate_by = 10
    ordering = ['-date']


class TournamentDetails(DetailView, MultipleObjectMixin):
    model = Tournament
    template_name = "../templates/tournament.html"
    paginate_by = 1  # TODO: change this
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        object_list = Game.objects.filter(tournament_id=self.object.id).order_by("-id")
        context = super(TournamentDetails, self).get_context_data(object_list=object_list, **kwargs)
        return context


class GamesList(ListView):
    model = Game
    template_name = "../templates/index.html"
    paginate_by = 5
    ordering = ['id']


class GameDetails(DetailView):
    model = Game
    template_name = "../templates/game.html"


# class GameDetailsTest(DetailView):
#     model = Game
#     http_method_names = ['get', ]
#
#     def get(self, request, *args, **kwargs):
#         data = Game.objects.filter(id=id).values()
#         data = serializers.serialize("json", data)
#         return JsonResponse(data, status=200, safe=False)


# TODO: convert this somehow to class view
def game_details_json(request, pk):
    try:
        data = Game.objects.get(id=pk)
        data = serializers.serialize("json", [data])
        # need to get pgn also
        return JsonResponse(data, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error" : str(e)}, status=200, safe=False)

