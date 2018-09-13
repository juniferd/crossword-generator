var Button = require('../Button/Button');
var List = require('./List');

var utils = require("common/util");

$C("Button", function(m) {
  utils.inject_css("scoped_Button", m.css);
});

class MyComponent extends React.Component{

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

    this.cell_changed(j, i);
    // switch direction if clicking on the same square
    if (j == y && i == x) {
      this.setState({ isDown: !this.state.isDown });
    }
    e.target.setSelectionRange(0, 10);
  }

  onKeydown(j, i, e) {
    // TODO: detect backspace and move forward
  }

  onChanged(j, i, e) {
    const { board } = this.state;
    // only can have one letter at a time in the board
    let val = e.target.value;
    if (val) {
      val = val[val.length-1];
    } else {
      val = "";
    }

    board[j][i] = val;
    this.setState({ board });
    e.target.value = val;
    // this.forceUpdate();
  }

  cell_changed(y, x) {
    this.setState({
      x: x,
      y: y
    });
  }

  getSuggestions() {
    console.log("GETTING SUGGESTIONS FOR WORD AT", this.state.x, this.state.y);

    this.rpc.get_suggestions(this.state.board, this.state.x, this.state.y).done(function(res, err) {
      this.setState({ suggestions: res });
      console.log("RES", res);
    });

  }

  toggleSquare() {

  }
  getCellClass(j, i, cellVal) {
    const { x, y, isDown } = this.state;
    let classes = 'cell';

    if ((j == y && isDown) ||
      (i == x && !isDown)) {
        classes += " highlight";
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
              return <input type='text'
                key={i}
                className={ this.getCellClass(j, i, board[j][i]) }
                onKeydown={(e) => { this.onKeydown(j, i, e) }}
                onChange={(e) => { this.onChanged(j, i, e) }}
                onClick={(e) => { this.onClicked(j, i, e) }} value={board[j][i]}/ >
            })
          }
        </div>
      );
    });

    return (
      <div>
        <div className='crossword'>
            { rows }
        </div>
        <Button className="scoped_Button" style="display: none;"
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

module.exports = MyComponent;
