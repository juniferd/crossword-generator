var React = $require("react");
const ButtonCss = require('Button/Button.sass')

class Button extends React.Component {
  constructor(props) {
    super(props);
  }

  onClick() {
    console.log('default click');
  }
  render() {
    const {
      className,
      isDisabled,
      onClick,
      text,
    } = this.props;
    const onClickHandler = onClick ? onClick : this.onClick;
    return (
      <div>
        <button
          className={ButtonCss.className}
          onClick={onClickHandler}
          disabled={isDisabled} >
          {text}
        </button>
      </div>
    );
  }
}

module.exports = Button;
