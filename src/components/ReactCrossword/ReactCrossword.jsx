class MyComponent extends React.Component{

  constructor(props){
    super(props);
    this.state = { board: props.board };
  }

  onClicked(j, i) {
    this.rpc.cell_changed(j, i);
  }

  onChanged(j, i, e) {
    console.log("THIS CELL CHANGED", j, i, e);
    this.state.board[j][i] = e.target.value;
  }

  cell_changed(x, y) {
    this.setState({
      x: x,
      y: y
    });
  }

  getSuggestions() {
    console.log("GETTING SUGGESTIONS FOR WORD AT", this.state.x, this.state.y);

    this.rpc.get_suggestions(this.state.board, this.state.x, this.state.y).done(function(res, err) {
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
            return <input type='text' className='cell'
              onChange={(e) => { self.onChanged(j, i, e) }}
              onClick={() => { self.onClicked(j, i) }} / >
          })
        }
      </div>);
    });

    return <div>
      <div className='crossword'>
          { rows }
      </div>

      <div className='controls mtl'>
        <div onClick={self.getSuggestions.bind(self)} >Get Suggestions</div>
        <div onClick={self.toggleSquare.bind(self)} >Block/Unblock Square</div>
      </div>
    </div>

  }

}

module.exports = MyComponent;
