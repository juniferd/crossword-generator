import flask
app = flask.Flask(__name__)

import crossword
import os

import pudgy

pudgy.register_blueprint(app)
pudgy.Component.set_base_dir(os.path.join(app.root_path, "components"))

class CrosswordComponent(pudgy.JinjaComponent, pudgy.SassComponent,
    pudgy.BackboneComponent, pudgy.ServerBridge):
    pass

class ReactCrossword(pudgy.ReactComponent, pudgy.SassComponent,
    pudgy.ServerBridge):
    pass

def cell_changed(cls, x, y):
    print("CELL CHANGED", x,y)
    cls.call("cell_changed", x, y);

ReactCrossword.api(cell_changed)
CrosswordComponent.api(cell_changed)



@CrosswordComponent.api
def rerender(cls, board):
    cw = crossword.Crossword()
    cw.board_height = len(board)
    cw.board_width = len(board[0])
    cw.board = board

    print "made crossword", cw

    cc = CrosswordComponent(crossword=cw)

    return cls.replace_html(cc.render())

@CrosswordComponent.api
def get_suggestions(cls, board, x, y):
    cw = crossword.Crossword()
    cw.board_height = len(board)
    cw.board_width = len(board[0])
    cw.board = board

    print("X, Y", x, y)

    print cw.board_height

    down = cw.get_letters((x, y), 'down')
    across = cw.get_letters((x, y), 'across')

    suggested = cw.suggest_words(across)
    suggested2 = cw.suggest_words(down)

    return {
        "across" : list(suggested),
        "down" : list(suggested2)
    }



@app.route('/')
def get_crossword():
    cw = crossword.Crossword()

    cc = ReactCrossword(board=cw.board)
#    cc = CrosswordComponent(crossword=cw)
    cc.set_ref("crossword")

    return flask.render_template("crossword.html", crossword=cc)

if __name__ == "__main__":
    app.run(port=3333)
