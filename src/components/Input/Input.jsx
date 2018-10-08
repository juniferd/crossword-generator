const React = $require('react');

class Input extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const {
      inputType,
      isChecked,
      text,
    } = this.props;
    return (
      <div>
        <input
          type={inputType}
          checked={isChecked}
        />
        {text}
      </div>
    )
  }
}

module.exports = Input;
