import datetime

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
    date_filter = django_filters.DateFilter(method='date_filter_method')
    tournament__type = django_filters.CharFilter(field_name='tournament', lookup_expr='type__exact')
    tournament__name = django_filters.CharFilter(field_name='tournament', lookup_expr='name__icontains')
    name_filter = django_filters.CharFilter(method='name_filter_method')
    club_filter = django_filters.CharFilter(method='club_filter_method')

    class Meta:
        model = Game
        fields = ['name_filter', 'date_filter', 'date', 'tournament__type', 'tournament__name']


    def date_filter_method(self, queryset, name, value: datetime.date):
        return queryset.filter(
            Q(date__year__exact=value.year) &
            Q(date__month__exact=value.month)
        )

    def name_filter_method(self, queryset, name, value):
        return queryset.filter(
            Q(white_player__last_name__icontains=value) |
            Q(black_player__last_name__icontains=value)
        )

    def club_filter_method(self, queryset, name, value):
        return queryset.filter(
            Q(white_player__club__icontains=value) |
            Q(black_player__club__icontains=value)
        )
