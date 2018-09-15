var React = require("vendor/react");

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
          className={className ? className : ''}
          onClick={onClickHandler}
          disabled={isDisabled}
        >
          {text}
        </button>
      </div>
    );
  }
}

module.exports = Button;
