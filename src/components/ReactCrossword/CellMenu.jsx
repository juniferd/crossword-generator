const React = require('vendor/react');
const Button = require('Button/Button.jsx');

const ButtonCss = require('Button/Button.sass')

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
          className={ButtonCss.className}
          onClick={insertColumn}
          text={'Insert column before'}
        />
        <Button
          className={ButtonCss.className}
          onClick={addColumn}
          text={'Insert column after'}
        />
        <Button
          className={ButtonCss.className}
          onClick={removeColumn}
          text={'Remove column'}
        />
        <Button
          className={ButtonCss.className}
          onClick={insertRow}
          text={'Insert row before'}
        />
        <Button
          className={ButtonCss.className}
          onClick={addRow}
          text={'Insert row after'}
        />
        <Button
          className={ButtonCss.className}
          onClick={removeRow}
          text={'Remove row'}
        />
      </div>
    );
  }
}

module.exports = CellMenu;
