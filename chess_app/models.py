from django.db import models

from chess_app.lookups import OnlyYearAndMonth


class Parse(models.Model):
    upload = models.FileField(upload_to="")

    def __str__(self):
        return '%s' % (self.upload)


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, null=True)
    type = models.CharField(max_length=1, null=True)
    time = models.DecimalField(max_digits=5, decimal_places=1, default=0, null=True)
    time_add = models.DecimalField(max_digits=5, decimal_places=1, default=0, null=True)
    date = models.DateField(null=True)
    city = models.CharField(max_length=50, null=True)
    link = models.CharField(max_length=200, null=True)

    models.DateField.register_lookup(OnlyYearAndMonth)


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    club = models.CharField(max_length=50, null=True)


class PGN(models.Model):
    pgn = models.TextField(max_length=5000)


class Game(models.Model):
    white_player = models.ForeignKey(Player, related_name='white', on_delete=models.CASCADE)
    black_player = models.ForeignKey(Player, related_name='black', on_delete=models.CASCADE)
    date = models.DateField(null=True)
    result = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    round = models.IntegerField(default=1, null=True)
    pgn = models.ForeignKey(PGN, on_delete=models.CASCADE, null=True)
    preview = models.TextField(max_length=100, null=True)


