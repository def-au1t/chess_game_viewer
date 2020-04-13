from rest_framework.serializers import ModelSerializer
from chess.models import Tournament, Game, PGN, Player


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class PGNSerializer(ModelSerializer):
    class Meta:
        model = PGN
        fields = '__all__'


class TournamentSerializer(ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['pgn'] = PGNSerializer(instance.pgn).data
        response['black_player'] = PlayerSerializer(instance.black_player).data
        response['white_player'] = PlayerSerializer(instance.white_player).data
        response['tournament'] = TournamentSerializer(instance.tournament).data
        return response
