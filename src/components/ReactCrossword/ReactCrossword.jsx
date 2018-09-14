var Button = require('Button/Button.jsx');
var List = require('./List.jsx');
var React = require("vendor/react");

var cssUtils = require("common/css_utils");
var WaitForCss = cssUtils.WaitForCss;
var ScopedCss = cssUtils.ScopedCss;

export default class MyComponent extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      board: props.board,
      hist: {},
      isAcross: true,
      suggestions: {},
    };

    var self = this;
    _.each(self.state.board, function(row, j) {
      self.state.hist[j] = {};
      _.each(row, function(cell, i) {
        self.state.hist[j][i] = {};
      });
    });

  }

  componentDidUpdate(prevProps, prevState) {
    console.log('component did update now', this.props, this.state);
  }

  onClicked(j, i, e) {
    const {
      x,
      y,
      isAcross,
    } = this.state;



    this.setState({ x: i, y: j });
    // switch direction if clicking on the same square
    if (j == y && i == x) {
      this.setState({ isAcross: !this.state.isAcross });
    }
  }

  onKeyDown(e) {
    var s = String.fromCharCode(e.keyCode);
    var isLetter = s.match(/[a-z]/i);

    console.log("PRESSED",e.keyCode);

    // keycode 8 = backspace
    // keycode 9 = tab
    // keycode 65 to 128 is characters
    // keycode 33 to 65 is symbols or something
    var inc = 1;
    var character;
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

    var board = this.state.board;
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

    var isAcross = this.state.isAcross;
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

        this.setState({ suggestions: res });
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

  render() {
    const { board, x, y, isAcross, suggestions } = this.state;
    var hist = this.state.hist;
    const rows = board.map((row, j) => {
      return (
        <div className='row' key={j}>
          {
            row.map((cell, i) => {
              return <span type='text'
                key={i}
                className={ this.getCellClass(j, i, board[j][i]) }
                onClick={(e) => { this.onClicked(j, i, e) }}>

                {board[j][i]}


                <span className='heatmap'>
                  {hist[j][i]['across']? "a:" + hist[j][i].across : ""}
                  <div> </div>
                  {hist[j][i]['down']? "d:" + hist[j][i].down : ""}
                </span>


              </span>
            })
          }
        </div>
      );
    });

    return (
      <div className={WaitForCss("Button")}>
        <div className='crossword noselect' onKeyDown={(e) => { this.onKeyDown(e) }} tabIndex="0" >
            { rows }
        </div>
        <Button className={ScopedCss("Button")}
          onClick={() => this.getSuggestions()}
          text={'Fetch Suggestions'} />
        <Button className={ScopedCss("Button")}
          onClick={() => this.validateBoard()}
          text={'Validate Board'} />
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
