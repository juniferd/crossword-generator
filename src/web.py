import flask
import models
import time
app = flask.Flask(__name__)

import crossword
import os

import pudgy

pudgy.register_blueprint(app)
pudgy.Component.set_base_dir(os.path.join(app.root_path, "components"))

import dukpy
def jsx_compile(data, fname):
    return dukpy.jsx_compile(data)

pudgy.ReactComponent.set_jsx_compiler(jsx_compile)
# pudgy.ReactComponent.add_babel_presets("@babel/preset-env")

class CrosswordComponent(pudgy.JinjaComponent, pudgy.SassComponent,
    pudgy.BackboneComponent, pudgy.ServerBridge):
    pass

class ReactCrossword(pudgy.ReactComponent, pudgy.SassComponent,
    pudgy.ServerBridge):
    pass

class Button(pudgy.ReactComponent, pudgy.SassComponent):
    pass

def cell_changed(cls, x, y):
    print("CELL CHANGED", x,y)
    cls.call("cell_changed", x, y);

def rerender(cls, board):
    cw = crossword.Crossword()
    cw.board_height = len(board)
    cw.board_width = len(board[0])
    cw.board = board

    print "made crossword", cw

    cc = CrosswordComponent(crossword=cw)

    return cls.replace_html(cc.render())


def build_crossword(board):
    cw = crossword.Crossword()
    cw.board_height = len(board)
    cw.board_width = len(board[0])
    cw.board = board
    return cw

def remove_row(cls, board, row):
    new_board = board[:row] + board[row+1:]
    cw = build_crossword(new_board)
    return {
        "board": cw.board
    }

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

def remove_column(cls, board, col):
    new_board = []
    for row in board:
        new_row = row[:col] + row[col+1:]
        new_board.append(new_row)
    cw = build_crossword(new_board)
    return {
        "board": cw.board
    }

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

def get_all_suggestions(cls, board):
    cw = build_crossword(board)
    return {
        "squares" : cw.get_start_squares()
    }


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

def update_board(cls, board, boardId):
    s = board_to_str(board)
    c = models.Board.select().where(models.Board.id == boardId).get()
    c.board = s
    c.save()
    print c.board
    return {
        "success": True
    }

def save_board(cls, board):
    s = board_to_str(board)
    b = models.Board.create(board=s, created_at=time.time())
    return {
        "boardId": b.id,
        "boardUrl" : flask.url_for('get_crossword', id=b.id)
    }

@app.route('/crossword/<id>')
def get_crossword(id):
    c = models.Board.select().where(models.Board.id == id).get()
    print c.board
    cw = crossword.Crossword()
    if type(c.board) == str or type(c.board) == unicode:
        board = [ list(row) for row in c.board.split('\n') ]
        cw.board = board
        cw.board_height = len(board)
        cw.board_length = len(board[0])

    print type(c.board)

    cc = ReactCrossword(board=cw.board, boardId=id)
    cc.set_ref("crossword")

    return flask.render_template("crossword.html", crossword=cc)

@app.route('/')
def get_index():
    cw = crossword.Crossword()

    cc = ReactCrossword(board=cw.board)
#    cc = CrosswordComponent(crossword=cw)
    cc.set_ref("crossword")

    return flask.render_template("crossword.html", crossword=cc)

API = [ get_suggestions, get_all_suggestions, rerender, cell_changed, insert_row, insert_column, remove_row, remove_column, save_board, update_board ]
for a in API:
    CrosswordComponent.api(a)
    ReactCrossword.api(a)

if __name__ == "__main__":
    app.run(port=3333)
