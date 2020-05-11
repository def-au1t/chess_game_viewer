import django_filters

from chess_app.models import Tournament, Game


class TournamentsListFilter(django_filters.FilterSet):
    class Meta:
        model = Tournament
        fields = {
            "name": ["icontains"],
            "date": ["ym"],
            "city": ["icontains"],
            "time": ["exact"],
            "type": ["exact"]
        }


class GamesListFilter(django_filters.FilterSet):
    class Meta:
        model = Game
        fields = {
            "tournament__date": ["ym"],
            "tournament__name": ["icontains"],
            "tournament__type": ["exact"]

        }