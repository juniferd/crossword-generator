module.exports = {
  events: {
    "click .cell" : "handle_cell_clicked"
  },
  handle_cell_clicked: function(evt) {
    var clickedEl = $(evt.target);
    console.log("CELL CLICKED", clickedEl);
    var x = clickedEl.data("x");
    var y = clickedEl.data("y");
    console.log(this, x, y);

    this.rpc.cell_changed(x, y).done(function(err, res) {
      if (!err) {
        console.log("WORDS ARE",res);
      }
    });

  },
  initialize: function() {
    console.log("LOADED COMPONENT", this);
  }

};
