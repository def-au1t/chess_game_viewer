import io
import chess.pgn

from chess_app.models import Player


def get_data(file):
    # Open image file for reading (binary mode)
    pgn = open(file)
    pgns = []
    # Parse file

    game = chess.pgn.read_game(pgn)
    while game is not None:
        pgns.append(str(game))
        game = chess.pgn.read_game(pgn)
    # meta = {'first_name': first_game.headers["White"], 'last_name': first_game.headers["White"]}

    meta = {'pgn': pgns}

    # create dictionary to receive data
    # meta={}
    # meta['date'] = str(tags['EXIF DateTimeOriginal'].values)
    # meta['fnumber'] = str(tags['EXIF FNumber'])
    # meta['exposure'] = str(tags['EXIF ExposureTime'])
    # meta['iso'] = str(tags['EXIF ISOSpeedRatings'])
    # meta['camera'] =str( tags['Image Model'].values)

    return meta


def get_player_data(data):
    game = chess.pgn.read_game(io.StringIO(data))
    name = game.headers["White"].split(',')
    last_name = name[0]
    first_name = name[1]
    obj, created = Player.objects.get_or_create(first_name=first_name, last_name=last_name)
    name = game.headers["Black"].split(',')
    last_name = name[0]
    first_name = name[1]
    obj, created = Player.objects.get_or_create(first_name=first_name, last_name=last_name)
