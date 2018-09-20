const React = require("vendor/react");
const List = require('./List.jsx');
const CellMenu = require('./CellMenu.jsx');

const Button = require('Button/Button.jsx');

const resetHist = (board) => {
  const hist = {};
  _.each(board, function(row, j) {
    hist[j] = {};
    _.each(row, function(cell, i) {
      hist[j][i] = {};
    });
  });
  return hist;
};

export default class MyComponent extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      board: props.board,
      hist: resetHist(props.board),
      isAcross: true,
      isFetchingSuggestions: false,
      suggestions: {},
      boardId: props.boardId,
    };

  }

  componentDidUpdate(prevProps, prevState) {
    console.log('component did update now', this.props, this.state);
  }

  onClicked(j, i) {
    const {
      isAcross,
      x,
      y,
    } = this.state;

    this.setState({ x: i, y: j });
    // switch direction if clicking on the same square
    if (j == y && i == x) {
      this.setState({ isAcross: !this.state.isAcross });
    }
  }

  onKeyDown(e) {
    const { board } = this.state;
    let s = String.fromCharCode(e.keyCode);
    let isLetter = s.match(/[a-z]/i);

    console.log("PRESSED",e.keyCode);

    // keycode 8 = backspace
    // keycode 9 = tab
    // keycode 65 to 128 is characters
    // keycode 33 to 65 is symbols or something
    let inc = 1;
    let character;
    // TODO: arrow keys should navigate around without entering character
    if (e.keyCode < 65) {
      character = '#';
      if (e.keyCode == 8) {
        character = '_';
        inc = -1;
      } else if (e.keyCode == 9) {
        this.state.isAcross = !this.state.isAcross;
        e.preventDefault();
        this.forceUpdate();
        return;
      } else if (e.keyCode < 30) {
        return;
      }

    } else if (isLetter) {
      character = s;
    }

    if (!character) {
      return;
    }

    this.state.board[this.state.y][this.state.x] = character;

    if (this.state.isAcross)  {
      this.state.x += inc;
    } else {
      this.state.y += inc;
    }

    // snap state to board perimeter
    if (this.state.x < 0) { this.state.x = 0; }
    if (this.state.y < 0) { this.state.y = 0; }

    if (this.state.x >= board[0].length) { this.state.x = board[0].length - 1; }
    if (this.state.y >= board.length) { this.state.y = board.length - 1; }

    this.forceUpdate();
  }

  validateBoard() {
    var self = this;
    self.state.hist = {};

    this
      .rpc
      .get_all_suggestions(this.state.board)
      .done(function(res, err) {
        _.each(self.state.board, function(row, j) {
          self.state.hist[j] = {};
          _.each(row, function(cell, i) {
            self.state.hist[j][i] = {};
          });
        });

        _.each(res.squares, function(v, k) {
          const [x, y, d] = k.split(",");

          if (!self.state.hist[y]) {
            self.state.hist[y] = [];
          }

          if (!self.state.hist[y][x]) {
            self.state.hist[y][x] = {};
          }

          self.state.hist[y][x][d] = v;

        });

        self.forceUpdate();

      });

  }

  getSuggestions() {
    console.log("GETTING SUGGESTIONS FOR WORD AT", this.state.x, this.state.y);

    const { isAcross } = this.state;
    this.setState({ isFetchingSuggestions: true });

    this
      .rpc
      .get_suggestions(this.state.board, this.state.x, this.state.y)
      .kwargs({ down: !this.state.isAcross, across: this.state.isAcross})
      .done(function(res, err) {
        if (isAcross) {
          res.down = null;
        } else {
          res.across = null;
        }

        this.setState({ suggestions: res, isFetchingSuggestions: false });
    });

  }

  getCellClass(j, i, cellVal) {
    const { x, y, isAcross } = this.state;
    let classes = 'cell';

    if ((j == y && isAcross) ||
      (i == x && !isAcross)) {
        classes += " highlight";
    }

    if (j == y && i == x) {
      classes += " focused";
    }

    if (cellVal == '#') {
      classes += ' blocked'
    }
    return classes;
  }

  removeRow(row) {
    this
      .rpc
      .remove_row(this.state.board, row)
      .done((res, err) => {
        if (!err) {
          this.setState({ board: res.board, hist: resetHist(res.board) });
        } else {
          console.log('error', err);
        }
      });
  }
  addRow(row, dir='after') {
    this
      .rpc
      .insert_row(this.state.board, row, dir)
      .done((res, err) => {
        if (!err) {
          this.setState({ board: res.board, hist: resetHist(res.board) });
        } else {
          console.log('error', err);
        }
      });
  }
  removeColumn(col) {
    this
      .rpc
      .remove_column(this.state.board, col)
      .done((res, err) => {
        if (!err) {
          this.setState({ board: res.board, hist: resetHist(res.board) });
        } else {
          console.log('error', err);
        }
      });
  }
  addColumn(col, dir='after') {
    this
      .rpc
      .insert_column(this.state.board, col, dir)
      .done((res, err) => {
        if (!err) {
          this.setState({ board: res.board, hist: resetHist(res.board) });
        } else {
          console.log('error', err);
        }
      });
  }
  saveBoard() {
    const { boardId, board } = this.state;
    if (boardId) {
      // update board
      this
        .rpc
        .update_board(board, boardId)
        .done((res, err) => {
          if (!err) {
            console.log('success', res);
          } else {
            console.log('error', err);
          }
        });
    } else {
      // save new board
      this
        .rpc
        .save_board(this.state.board)
        .done((res, err) => {
          if (!err) {
            this.setState({ boardId: res.boardId });
            window.history.pushState({}, 'test', res.boardUrl);
          } else {
            console.log('error', err);
          }
        });
    }
  }

  render() {
    const {
      board,
      hist,
      isAcross,
      isFetchingSuggestions,
      suggestions,
      x,
      y,
      isCellMenuVisible,
    } = this.state;
    const rows = board.map((row, j) => {
      return (
        <div className='row' key={j}>
          {
            row.map((cell, i) => {
              return <div type='text'
                key={i}
                className={ this.getCellClass(j, i, board[j][i]) }
                onClick={(e) => { this.onClicked(j, i) }}>

                {board[j][i]}

                <span className='heatmap'>
                  {hist[j][i]['across']? "a:" + hist[j][i].across : ""}
                  <div> </div>
                  {hist[j][i]['down']? "d:" + hist[j][i].down : ""}
                </span>
              </div>
            })
          }
        </div>
      );
    });

    return (
      <div>
        <div className='crossword noselect' onKeyDown={(e) => { this.onKeyDown(e) }} tabIndex="0" >
            { rows }
            <Button
              onClick={() => this.setState({ isCellMenuVisible: !isCellMenuVisible})}
              text={isCellMenuVisible ? 'Hide cell menu' : 'Show cell menu'}
            />
            <CellMenu
              isVisible={isCellMenuVisible}
              x={x}
              y={y}
              addColumn={() => this.addColumn(x)}
              insertColumn={() => this.addColumn(x, 'before')}
              removeColumn={() => this.removeColumn(x)}
              addRow={() => this.addRow(y)}
              insertRow={() => this.addRow(y, 'before')}
              removeRow={() => this.removeRow(y)}
            />
        </div>
        <Button
          onClick={() => this.getSuggestions()}
          isDisabled={isFetchingSuggestions}
          text={'Fetch Suggestions'} />
        <Button
          onClick={() => this.validateBoard()}
          text={'Validate Board'} />
        <Button
          onClick={() => this.saveBoard()}
          text={'Save'} />
        <List
          title={'Across suggestions'}
          suggestions={suggestions.across} />
        <List
          title={'Down suggestions'}
          suggestions={suggestions.down} />
      </div>
    );
  }
}
