from django import forms

from chess_app.models import PGN


class PgnForm(forms.ModelForm):

    class Meta:
        model = PGN
        fields = ('pgn',)