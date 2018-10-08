import crossword
import models
import flask
import pudgy
import dukpy

class ReactCrossword(pudgy.ReactComponent, pudgy.SassComponent,
    pudgy.ServerBridge):
    pass

@ReactCrossword.api
def cell_changed(cls, x, y):
    print("CELL CHANGED", x,y)
    cls.call("cell_changed", x, y);

@ReactCrossword.api
def rerender(cls, board):
    cw = crossword.Crossword()
    cw.board_height = len(board)
    cw.board_width = len(board[0])
    cw.board = board

    print "made crossword", cw

    cc = CrosswordComponent(crossword=cw)

    return cls.replace_html(cc.render())

@ReactCrossword.api
def load_board(cls, id):
    try:
        c = models.Board.select().where(models.Board.id == id).dicts().get()
    except:
        c = models.Board.select().where(models.Board.id == 1).dicts().get()
    cw = build_crossword(c["board"])

    return {
        "url" : flask.url_for('get_crossword', id=c["id"]),
        "board" : cw.board,
        "id": c["id"]
    }

def build_crossword(board):
    if type(board) == str or type(board) == unicode:
        board = [ list(row) for row in board.split('\n') ]
    cw = crossword.Crossword()
    cw.board_height = len(board)
    cw.board_width = len(board[0])
    cw.board = board
    return cw

@ReactCrossword.api
def remove_row(cls, board, row):
    new_board = board[:row] + board[row+1:]
    cw = build_crossword(new_board)
    return {
        "board": cw.board
    }

@ReactCrossword.api
def insert_row(cls, board, row, direction):
    new_board = []
    for i in xrange(len(board)):
        if i == row and direction == 'before':
            new_board.append(["_"] * len(board[i]))
        new_board.append(board[i])
        if i == row and direction == 'after':
            new_board.append(["_"] * len(board[i]))
    cw = build_crossword(new_board)
    return {
        "board": cw.board
    }

@ReactCrossword.api
def remove_column(cls, board, col):
    new_board = []
    for row in board:
        new_row = row[:col] + row[col+1:]
        new_board.append(new_row)
    cw = build_crossword(new_board)
    return {
        "board": cw.board
    }

@ReactCrossword.api
def insert_column(cls, board, col, direction):
    new_board = []
    for row in board:
        new_row = []
        for i in xrange(len(row)):
            if i == col and direction == 'before':
                new_row.append("_")
            new_row.append(row[i])
            if i == col and direction == 'after':
                new_row.append("_")
        new_board.append(new_row)
    cw = build_crossword(new_board)
    return {
        "board": cw.board
    }

@ReactCrossword.api
def get_all_suggestions(cls, board):
    cw = build_crossword(board)
    return {
        "squares" : cw.get_start_squares()
    }


@ReactCrossword.api
def get_suggestions(cls, board, x, y, down=False, across=False):
    cw = build_crossword(board)

    possible = []
    possible2 = []

    if across:
        s = cw.get_start_of_word([x, y], 'across')
        across = cw.get_letters(s, 'across')
        suggested = cw.suggest_words(across)
        possible = cw.filter_suggested(suggested, s, 'across')

    if down:
        s = cw.get_start_of_word([x, y], 'down')
        down = cw.get_letters(s, 'down')
        suggested2 = cw.suggest_words(down)
        possible2 = cw.filter_suggested(suggested2, s, 'down')

    return {
        "across" : list(possible),
        "down" : list(possible2)
    }

def board_to_str(board):
    s = []
    for row in board:
        s.append(''.join(row))
    s = '\n'.join(s)
    return s

@ReactCrossword.api
def update_board(cls, board, boardId):
    s = board_to_str(board)
    c = models.Board.select().where(models.Board.id == boardId).get()
    c.board = s
    c.save()
    print c.board
    return {
        "success": True
    }

@ReactCrossword.api
def save_board(cls, board):
    s = board_to_str(board)
    b = models.Board.create(board=s, created_at=time.time())
    return {
        "boardId": b.id,
        "boardUrl" : flask.url_for('get_crossword', id=b.id)
    }

