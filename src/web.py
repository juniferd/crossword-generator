import flask
app = flask.Flask(__name__)

import crossword
import os

import pudgy

pudgy.register_blueprint(app)
pudgy.Component.set_base_dir(os.path.join(app.root_path, "components"))

pudgy.ReactComponent.add_babel_presets("@babel/preset-env")

class CrosswordComponent(pudgy.JinjaComponent, pudgy.SassComponent,
    pudgy.BackboneComponent, pudgy.ServerBridge):
    pass

class ReactCrossword(pudgy.ReactComponent, pudgy.SassComponent,
    pudgy.ServerBridge):
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

def get_suggestions(cls, board, x, y):
    cw = crossword.Crossword()
    cw.board_height = len(board)
    cw.board_width = len(board[0])
    cw.board = board

    print("X, Y", x, y)

    s = cw.get_start_of_word([x, y], 'across')
    across = cw.get_letters(s, 'across')

    suggested = cw.suggest_words(across)
    possible = cw.filter_suggested(suggested, s, 'across')

    s = cw.get_start_of_word([x, y], 'down')
    down = cw.get_letters(s, 'down')
    suggested2 = cw.suggest_words(down)
    possible2 = cw.filter_suggested(suggested2, s, 'down')

    return {
        "across" : list(possible),
        "down" : list(possible2)
    }

@app.route('/')
def get_crossword():
    cw = crossword.Crossword()

    cc = ReactCrossword(board=cw.board)
#    cc = CrosswordComponent(crossword=cw)
    cc.set_ref("crossword")

    return flask.render_template("crossword.html", crossword=cc)

API = [ get_suggestions, rerender, cell_changed ]
for a in API:
    CrosswordComponent.api(a)
    ReactCrossword.api(a)

if __name__ == "__main__":
    app.run(port=3333)
