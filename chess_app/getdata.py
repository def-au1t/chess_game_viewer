import io
import chess.pgn
import datetime
import os

from chess_app.models import Player, Tournament, PGN, Game, Parse
from dateutil.parser import parse
from decimal import Decimal


def get_data(file, request):
    pgn = open(file, encoding="utf-8-sig")
    pgns = []

    game = chess.pgn.read_game(pgn)
    t_name = game.headers.get("Event", "?")
    t_date = game.headers.get("EventDate", "????.??.??")
    t_city = game.headers.get("Site", "?")
    request.session['t_name'] = t_name
    request.session['t_date'] = t_date
    request.session['t_city'] = t_city
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


def get_player_data(name, team):
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
    if team != "?" and team is not None:
        player.club = team
        player.save()
    return player


def get_tournament_data(t_cd):
    name = t_cd.get('name')
    description = t_cd.get('description')
    type = t_cd.get('type')
    time = t_cd.get('time')
    time_add = t_cd.get('time_add')
    date = t_cd.get('date')
    city = t_cd.get('city')
    link = t_cd.get('link')
    if name != "?" and name != "" and name is not None:
        tournament, created = Tournament.objects.get_or_create(name=name)
        tournament.date = date
        tournament.description = description
        tournament.type = type
        tournament.time = Decimal(time)
        tournament.time_add = Decimal(time_add)
        tournament.city = city
        tournament.link = link
        tournament.save()
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
                               round=round, pgn=pgn, preview=str(game.mainline_moves())[0:100] + "...")


def parse_data(data, tournament):
    game = chess.pgn.read_game(io.StringIO(data))
    date_str = game.headers.get("Date", "?")
    try:
        date = parse(date_str).date()
        if date.year < 1950:
            date = None
            game.headers["Date"] = ""
    except ValueError:
        date = None
        eventDate =  game.headers.get("EventDate", "?")
        if eventDate != "?":
            date = eventDate
            game.headers["Date"] = eventDate
        elif tournament and tournament.date:
            date = tournament.date
            game.headers["Date"] = tournament.date
        else:
            game.headers["Date"] = ""
            date = None
    if tournament and not tournament.date and date:
        tournament.date = date
        tournament.save()
    data = game
    pgn, created = PGN.objects.get_or_create(pgn=data)
    name = game.headers.get("White", "?").split(',')
    team = game.headers.get("WhiteTeam", "?")
    white_player = get_player_data(name, team)
    name = game.headers.get("Black", "?").split(',')
    team = game.headers.get("BlackTeam", "?")
    black_player = get_player_data(name, team)
    get_game_data(white_player, black_player, tournament, pgn, game, date)
