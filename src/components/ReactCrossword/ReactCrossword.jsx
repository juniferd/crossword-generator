var Button = require('Button/Button');
var List = require('./List');
var React = require("vendor/react");

var cssUtils = require("common/css_utils");
var WaitForCss = cssUtils.WaitForCss;
var ScopedCss = cssUtils.ScopedCss;

export default class MyComponent extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      board: props.board,
      isDown: true,
      suggestions: {},
    };
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('component did update now', this.props, this.state);
  }

  onClicked(j, i, e) {
    const {
      x,
      y,
      isDown,
    } = this.state;



    this.setState({ x: i, y: j });
    // switch direction if clicking on the same square
    if (j == y && i == x) {
      this.setState({ isDown: !this.state.isDown });
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
        this.state.isDown = !this.state.isDown;
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

    if (this.state.isDown)  {
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

  getSuggestions() {
    console.log("GETTING SUGGESTIONS FOR WORD AT", this.state.x, this.state.y);

    var isDown = this.state.isDown;
    this.rpc.get_suggestions(this.state.board, this.state.x, this.state.y).done(function(res, err) {
      console.log("RES", res);

      if (isDown) {
        res.down = null;
      } else {
        res.across = null;
      }

      this.setState({ suggestions: res });
    });

  }

  getCellClass(j, i, cellVal) {
    const { x, y, isDown } = this.state;
    let classes = 'cell';

    if ((j == y && isDown) ||
      (i == x && !isDown)) {
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
    const { board, x, y, isDown, suggestions } = this.state;
    const rows = board.map((row, j) => {
      return (
        <div className='row' key={j}>
          {
            row.map((cell, i) => {
              return <span type='text'
                key={i}
                className={ this.getCellClass(j, i, board[j][i]) }
                onClick={(e) => { this.onClicked(j, i, e) }}> {board[j][i]} </span>
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
