class MyComponent extends React.Component{

  constructor(props){
    super(props);
    this.state = { board: props.board, direction: 0  };
  }

  onClicked(j, i, e) {
    this.cell_changed(j, i);

    if (j == this.state.x && i == this.state.y) {
      this.state.direction = !this.state.direction;
      this.getSuggestions();
    }

    e.target.setSelectionRange(0, 10);




  }

  onKeydown(j,i,e) {
    // TODO: detect backspace and move forward
  }

  onChanged(j, i, e) {
    // only can have one letter at a time in the board
    var val = e.target.value;
    if (val) {
      val = val[val.length-1];
    } else {
      val = "";
    }

    this.state.board[j][i] = val;
    e.target.value = val;
    this.forceUpdate();
  }

  cell_changed(x, y) {
    this.setState({
      x: x,
      y: y
    });
  }

  getSuggestions() {
    console.log("GETTING SUGGESTIONS FOR WORD AT", this.state.x, this.state.y);

    this.rpc.get_suggestions(this.state.board, this.state.y, this.state.x).done(function(res, err) {
      console.log("RES", res);
    });

  }

  toggleSquare() {

  }

  render() {
    var board = this.state.board;
    var self = this;
    var rows = board.map(function(row, i) {
      return (<div className='row'>
        {
          row.map(function(cell, j) {
            var classes = "cell ";
            if ((j == self.state.x && self.state.direction) ||
                (i == self.state.y && !self.state.direction)) {
              classes += " highlight";
            }

            if (board[j][i] == '#') {
              classes += ' blocked'
            }

            return <input type='text' className={classes}
              onKeydown={(e) => { self.onKeydown(j,i,e) }}
              onChange={(e) => { self.onChanged(j, i, e) }}
              onClick={(e) => { self.onClicked(j, i, e) }} value={board[j][i]}/ >
          })
        }
      </div>);
    });

    return <div>
      <div className='crossword'>
          { rows }
      </div>

    </div>

  }

}

module.exports = MyComponent;
