import io
import chess.pgn
import datetime
import os

from chess_app.models import Player, Tournament, PGN, Game, Parse
from dateutil.parser import parse


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
    if len(name) == 0 or name[0] == "?":
        last_name = "Nieznany"
        first_name = "Zawodnik"
    else:
        last_name = name[0]
        if len(name) == 2:
            first_name = name[1]
        else:
            first_name = ""
    player, created = Player.objects.get_or_create(first_name=first_name, last_name=last_name)
    return player


def get_tournament_data(game, date):
    name = game.headers.get("Event", "?")

    if name != "?":
        tournament, created = Tournament.objects.get_or_create(name=name, date=date)
        return tournament
    else:
        return None


def get_game_data(white_player, black_player, tournament, pgn, game, date):
    result_str = game.headers.get("Result", "*")
    if result_str == "1-0":
        result = 1.0
    elif result_str == "0-1":
        result = 0.0
    elif result_str == "*" or result_str == "?":
        result = None
    else:
        result = 0.5
    round_str = game.headers.get("Round", "?")
    if round_str == "?":
        round = None
    else:
        round = float(round_str)
    Game.objects.get_or_create(white_player=white_player, black_player=black_player,
                               date=date, result=result, tournament=tournament,
                               round=round, pgn=pgn, preview=str(game.mainline_moves())[0:60]+"...")


def parse_data(data):
    game = chess.pgn.read_game(io.StringIO(data))
    date_str = game.headers.get("Date", "?")
    try:
        date = parse(date_str).date()
        if date.year < 1950:
            date = None
            game.headers["Date"] = ""
    except ValueError:
        date = None
        game.headers["Date"] = ""
    event_date_str = game.headers.get("EventDate", "????.??.??")
    try:
        event_date = parse(event_date_str).date()
        if event_date.year < 1950:
            event_date = None
            game.headers["EventDate"] = ""
    except ValueError:
        event_date = None
        game.headers["EventDate"] = ""
    data = game
    pgn, created = PGN.objects.get_or_create(pgn=data)
    name = game.headers.get("White", "?").split(',')
    white_player = get_player_data(name)
    name = game.headers.get("Black", "?").split(',')
    black_player = get_player_data(name)
    tournament = get_tournament_data(game, event_date)
    get_game_data(white_player, black_player, tournament, pgn, game, date)
