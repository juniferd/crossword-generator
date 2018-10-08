import flask
import models
import time
app = flask.Flask(__name__)

import crossword
import os

import pudgy
from crossword_component import ReactCrossword

pudgy.register_blueprint(app)

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

if __name__ == "__main__":
    app.run(port=3333)
