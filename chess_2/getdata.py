import chess.pgn


def get_player_data(file):
    # Open image file for reading (binary mode)
    pgn = open(file)

    # Parse file

    first_game = chess.pgn.read_game(pgn)
    # meta = {'first_name': first_game.headers["White"], 'last_name': first_game.headers["White"]}

    meta = {'pgn': first_game}

    # create dictionary to receive data
    # meta={}
    # meta['date'] = str(tags['EXIF DateTimeOriginal'].values)
    # meta['fnumber'] = str(tags['EXIF FNumber'])
    # meta['exposure'] = str(tags['EXIF ExposureTime'])
    # meta['iso'] = str(tags['EXIF ISOSpeedRatings'])
    # meta['camera'] =str( tags['Image Model'].values)

    return meta
