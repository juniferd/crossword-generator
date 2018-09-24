const React = $require('react');
const Button = require('Button/Button.jsx');

class CellMenu extends React.Component {
  constructor(props) {
    super(props);
  }

  getCss() {
    const { isVisible } = this.props;
    let css = "cellMenu ";
    return isVisible ? `${css} visible` : `${css} hidden`;
  }
  render() {
    const {
      x,
      y,
      insertColumn,
      addColumn,
      removeColumn,
      insertRow,
      addRow,
      removeRow,
    } = this.props;
    return (
      <div className={this.getCss()}
      >
        <Button
          onClick={insertColumn}
          text={'Insert column before'}
        />
        <Button
          onClick={addColumn}
          text={'Insert column after'}
        />
        <Button
          onClick={removeColumn}
          text={'Remove column'}
        />
        <Button
          onClick={insertRow}
          text={'Insert row before'}
        />
        <Button
          onClick={addRow}
          text={'Insert row after'}
        />
        <Button
          onClick={removeRow}
          text={'Remove row'}
        />
      </div>
    );
  }
}

module.exports = CellMenu;
