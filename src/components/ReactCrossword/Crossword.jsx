const React = $require("react");
const List = require('./List.jsx');
const CellMenu = require('./CellMenu.jsx');
const Button = require('Button/Button.jsx');
export function render() {
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
      <Button
        onClick={() => this.nextCrossword()}
        text={'Next'} />
      <List
        title={'Across suggestions'}
        suggestions={suggestions.across} />
      <List
        title={'Down suggestions'}
        suggestions={suggestions.down} />
    </div>
  );
}
