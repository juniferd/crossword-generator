var React = $require("react");

class List extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const {
      title,
      suggestions,
    } = this.props;
    return (
      <div className='suggestions'>
        <p>{ suggestions ? title : ""}</p>
        <ul>
          {
            suggestions && suggestions.map((item, i) => {
              return (
                <li key={i}>{ item }</li>
              )
            })
          }
        </ul>
      </div>
    );
  }
}

module.exports = List;
