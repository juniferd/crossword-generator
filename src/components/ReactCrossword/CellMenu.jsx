const React = require('vendor/react');
const Button = require('Button/Button.jsx');

const cssUtils = require('common/css_utils');
const WaitForCss = cssUtils.WaitForCss;
const ScopedCss = cssUtils.ScopedCss;

class CellMenu extends React.Component {
  constructor(props) {
    super(props);
  }

  getCss() {
    const { isVisible } = this.props;
    let css = `${WaitForCss('Button')} cellMenu`;
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
          className={ScopedCss('Button')}
          onClick={insertColumn}
          text={'Insert column before'}
        />
        <Button
          className={ScopedCss('Button')}
          onClick={addColumn}
          text={'Insert column after'}
        />
        <Button
          className={ScopedCss('Button')}
          onClick={removeColumn}
          text={'Remove column'}
        />
        <Button
          className={ScopedCss('Button')}
          onClick={insertRow}
          text={'Insert row before'}
        />
        <Button
          className={ScopedCss('Button')}
          onClick={addRow}
          text={'Insert row after'}
        />
        <Button
          className={ScopedCss('Button')}
          onClick={removeRow}
          text={'Remove row'}
        />
      </div>
    );
  }
}

module.exports = CellMenu;
