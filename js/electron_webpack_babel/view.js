'use strict';

const React = require('react');
const ReactDOM = require('react-dom');
import RaisedButton from 'material-ui/lib/raised-button';

class MyComponent extends React.Component {
  render() {
    return (
        <div>
          <div>Hello React + Material UI!</div>
          <RaisedButton label={"Button"} primary={true}/>
        </div>);
  }
}

var main = function() {
  ReactDOM.render(<MyComponent/>,
                  document.getElementById('view'));
};

main();
