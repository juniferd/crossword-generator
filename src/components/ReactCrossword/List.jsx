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
      <div>
        <p>{ title }</p>
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
