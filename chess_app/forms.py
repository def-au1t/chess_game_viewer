from django import forms
from chess_app.models import PGN, Tournament


class PgnForm(forms.ModelForm):
    class Meta:
        model = PGN
        fields = ('pgn',)


class TournamentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(TournamentForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['name'].required = False
        self.fields['type'].required = False

    class Meta:
        model = Tournament
        fields = ('name', 'description', 'type', 'time', 'time_add', 'date', 'city', 'link',)
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'type': 'Typ',
            'time': 'Czas',
            'time_add': 'Doliczony czas gry',
            'date': 'Data',
            'city': 'Miejscowość',
            'link': 'Link'
        }
        TYPE_CHOICES = (
            ('', 'Wybierz typ zawodów'),
            ('k', 'klasyczne'),
            ('s', 'szybkie'),
            ('b', 'błyskawiczne'),
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}),
            'time': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'time_add': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control',
                                           'placeholder': 'Select a date',
                                           'type': 'date'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
        }
