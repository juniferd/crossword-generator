module.exports = React.createClass({
  onClicked: function(j, i) {
    this.rpc.cell_changed(j, i);
  },
  cell_changed: function(x, y) {
    console.log("SERVER SAID CELL CHANGED", x, y);
  },
  render: function() {
    console.log("RENDERING", this.props.board);
    var self = this;
    var rows = this.props.board.map(function(row, i) {
      return (<div className='row'>
        {
          row.map(function(cell, j) {
            return <input type='text' className='cell'
              onClick={() => { self.onClicked(j, i) }} / >
          })
        }
      </div>);
    });

    return <div className='crossword'>
        { rows }
    </div>

  }
});
