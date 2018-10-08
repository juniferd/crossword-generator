export default function resetHist(board) {
  const hist = {};
  _.each(board, function(row, j) {
    hist[j] = {};
    _.each(row, function(cell, i) {
      hist[j][i] = {};
    });
  });
  return hist;
};
module.exports = resetHist;
