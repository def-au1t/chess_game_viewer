import io
import chess.pgn
import datetime
import os

from chess_app.models import Player, Tournament, PGN, Game, Parse


def get_data(file):
    pgn = open(file, encoding="utf-8-sig")
    pgns = []

    game = chess.pgn.read_game(pgn)
    while game is not None:
        pgns.append(str(game))
        game = chess.pgn.read_game(pgn)

    meta = {'pgn': pgns}

    pgn.close()
    if os.path.exists(file):
        os.remove(file)
    files = Parse.objects.all()
    for file in files:
        file.delete()
    return meta


def get_player_data(name):
    last_name = name[0]
    first_name = name[1]
    player, created = Player.objects.get_or_create(first_name=first_name, last_name=last_name)
    return player


def get_tournament_data(game):
    name = game.headers["Event"]
    date_str = game.headers["EventDate"]
    date = datetime.datetime.strptime(date_str, "%Y.%m.%d").date()
    tournament, created = Tournament.objects.get_or_create(name=name, date=date)
    return tournament


def get_game_data(white_player, black_player, tournament, pgn, game):
    result_str = game.headers["Result"]
    if result_str == "1-0":
        result = 1.0
    elif result_str == "0-1":
        result = 0.0
    else:
        result = 0.5
    date_str = game.headers["Date"]
    date = datetime.datetime.strptime(date_str, "%Y.%m.%d").date()
    round = game.headers["Round"]
    Game.objects.get_or_create(white_player=white_player, black_player=black_player,
                               date=date, result=result, tournament=tournament,
                               round=float(round), pgn=pgn, preview=game.mainline_moves())


def parse_data(data):
    pgn, created = PGN.objects.get_or_create(pgn=data)
    game = chess.pgn.read_game(io.StringIO(data))
    name = game.headers["White"].split(',')
    white_player = get_player_data(name)
    name = game.headers["Black"].split(',')
    black_player = get_player_data(name)
    tournament = get_tournament_data(game)
    get_game_data(white_player, black_player, tournament, pgn, game)
