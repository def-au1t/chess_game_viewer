import django_filters
from django.db.models import Q

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
    name_filter = django_filters.CharFilter(method='name_filter_method')
    club_filter = django_filters.CharFilter(method='club_filter_method')

    class Meta:
        model = Game
        fields = {
            "tournament__date": ["ym"],
            "tournament__name": ["icontains"],
            "tournament__type": ["exact"],
            "name_filter": ["name_filter"],
            "club_filter": ["club_filter"]

        }


    def name_filter_method(self, queryset, name, value):
        return Game.objects.filter(
            Q(white_player__last_name__icontains=value) |
            Q(black_player__last_name__icontains=value)
        )

    def club_filter_method(self, queryset, name, value):
        return Game.objects.filter(
            Q(white_player__club__icontains=value) |
            Q(black_player__club__icontains=value)
        )
