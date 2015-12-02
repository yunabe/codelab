require("./content.js")

const injectTapEventPlugin = require("react-tap-event-plugin");
injectTapEventPlugin();

const React = require('react');
const ReactDOM = require('react-dom');
const Dialog = require('material-ui/lib/dialog');
const FlatButton = require('material-ui/lib/flat-button');
const RaisedButton = require('material-ui/lib/raised-button');
const DropDownMenu = require('material-ui/lib/drop-down-menu');
const RadioButton = require('material-ui/lib/radio-button');
const RadioButtonGroup = require('material-ui/lib/radio-button-group');


const SHUFFLE_REPEAT = 100;

class FifteenState {
  constructor(n, pieceWidth) {
    this.n_ = n;
    this.pieceWidth = pieceWidth;
    this.state = new Array(n * n);
    for (var i = 0; i < n * n - 1; i++) {
      this.state[i] = i + 1;
    }
    this.state[n * n - 1] = 0;
    this.completed_ = true;

    this.settingShown = false;
    this.settingTitle = 'Settings';

    this.handlers_ = [];
  }

  resetBoard(n, pieceWidth) {
    this.n_ = n;
    this.pieceWidth = pieceWidth;
    this.state = new Array(n * n);
    for (var i = 0; i < n * n - 1; i++) {
      this.state[i] = i + 1;
    }
    this.state[n * n - 1] = 0;
    this.completed_ = true;
  }

  registerHandler(handler) {
    this.handlers_.push(handler);
  }

  checkCompleted() {
    var n  = this.n_;
    for (var i = 0; i < n * n - 1; i++) {
      if (this.state[i] != i + 1) {
        return false;
      }
    }
    return true;
  }

  showSetting() {
    this.settingShown = true;
    for (var i = 0; i < this.handlers_.length; i++) {
      this.handlers_[i]();
    }
  }

  hideSetting() {
    this.settingShown = false;
    for (var i = 0; i < this.handlers_.length; i++) {
      this.handlers_[i]();
    }
  }

  shuffle(repeat) {
    for (var i = 0; i < this.state.length - 1; i++) {
      this.state[i] = i + 1;
    }
    this.state[this.state.length - 1] = 0;
    var count = 0;
    while (count < repeat) {
      for (var pos = 0; this.state[pos] != 0; pos++) {}
      switch (Math.floor(Math.random() * 4)) {
      case 3:
        pos++;
        break;
      case 2:
        pos--;
        break;
      case 1:
        pos += this.n_;
        break;
      default:
        pos -= this.n_;
      }

      if (pos < 0 || pos >= this.state.length) {
        continue;
      }
      this.move(pos);
      count++;
    }
  }

  move(pos) {
    if (this.state[pos] == 0) {
      return;
    }
    var changed = this.moveLeft__(pos);
    changed = changed || this.moveRight__(pos);
    changed = changed || this.moveUp__(pos);
    changed = changed || this.moveDown__(pos);
    if (!changed) {
      return;
    }
    this.completed_ = this.checkCompleted();
    for (var i = 0; i < this.handlers_.length; i++) {
      this.handlers_[i]();
    }
  }

  moveLeft__(pos) {
    var zeroPos;
    for (zeroPos = pos - 1; Math.floor(zeroPos / this.n_) == Math.floor(pos / this.n_); zeroPos--) {
      if (this.state[zeroPos] != 0) {
        continue;
      }
      for (; zeroPos < pos; zeroPos++) {
        var tmp = this.state[zeroPos];
        this.state[zeroPos] = this.state[zeroPos + 1];
        this.state[zeroPos + 1] = tmp;
      }
      return true;
    }
    return false;
  }

  moveRight__(pos) {
    var zeroPos;
    for (zeroPos = pos + 1; Math.floor(zeroPos / this.n_) == Math.floor(pos / this.n_); zeroPos++) {
      if (this.state[zeroPos] != 0) {
        continue;
      }
      for (; zeroPos > pos; zeroPos--) {
        var tmp = this.state[zeroPos];
        this.state[zeroPos] = this.state[zeroPos - 1];
        this.state[zeroPos - 1] = tmp;
      }
      return true;
    }
    return false;
  }

  moveUp__(pos) {
    var zeroPos;
    for (zeroPos = pos - this.n_; zeroPos >= 0; zeroPos -= this.n_) {
      if (this.state[zeroPos] != 0) {
        continue;
      }
      for (; zeroPos < pos; zeroPos += this.n_) {
        var tmp = this.state[zeroPos];
        this.state[zeroPos] = this.state[zeroPos + this.n_];
        this.state[zeroPos + this.n_] = tmp;
      }
      return true;
    }
    return false;
  }

  moveDown__(pos) {
    var zeroPos;
    for (zeroPos = pos + this.n_; zeroPos < this.n_ * this.n_; zeroPos += this.n_) {
      if (this.state[zeroPos] != 0) {
        continue;
      }
      for (; zeroPos > pos; zeroPos -= this.n_) {
        var tmp = this.state[zeroPos];
        this.state[zeroPos] = this.state[zeroPos - this.n_];
        this.state[zeroPos - this.n_] = tmp;
      }
      return true;
    }
    return false;
  }
}

class FifteenBoard extends React.Component {
  render() {
    var posMap = {};
    for (var i = 0; i < this.props.state.state.length; i++) {
      posMap[this.props.state.state[i]] = i;
    }
    var pieces = [];
    for (var i = 1; i < size; i++) {
      pieces.push(<FifteenPiece key={i} number={i} pos={posMap[i]}
                                n={this.props.state.n_}
                                state={this.props.state}
                                pieceSize={this.props.pieceSize} />);
    }
    var width = this.props.state.pieceWidth * this.props.state.n_ + 'px';
    var style = {
      // This div is the origin point of children with position:absolute.
      'position': 'relative',
      'width': width,
      'height': width,
      'padding': '8px',
    };
    return <div style={style}>{pieces}</div>;
  }
}

class FifteenPiece extends React.Component {
  constructor() {
    // We do not need to pass params to the parent class because React framework
    // friendly fills the fields.
    super();
    this._onClick = this._onClick.bind(this);
  }

  render() {
    var pieceSize = this.props.state.pieceWidth;
    var pos = this.props.pos;
    var top = Math.floor(pos / this.props.n) * pieceSize + 'px';
    var left = pos % this.props.n * pieceSize + 'px';
    var number = this.props.number;
    var text = number == 0 ? '*' : String(number);
    var style = {
      'position': 'absolute',
      'top': '0',
      'left': '0',
      'WebkitTransform': 'translate(' + left + ',' + top + ')',
      'width': (pieceSize - 8)+ 'px',
      'height': (pieceSize - 8)+ 'px',
      'border': '1px solid',
      'WebkitTransition': '-webkit-transform 0.2s',
      'boxShadow': 'rgba(0, 0, 0, 0.317647) 0px 0px 3px 1px',
      'margin': '4px',
      'backgroundColor': '#fff',
      'fontFamily': 'Roboto, sans-serif',
      'fontSize': '25px',
      'textAlign': 'center',
      'borderRadius': '6px',
    };
    var this_ = this;
    return <div style={style} onTouchTap={this._onClick}>{text}</div>;
  }

  _onClick() {
    this.props.state.move(this.props.pos);
    if (this.props.state.completed_) {
      this.props.state.settingTitle = 'Congratulation!';
      this.props.state.showSetting();
    }
  }
}

class App extends React.Component {
  constructor() {
    super();
    this._onChange = this._onChange.bind(this);
    this._onShowSetting = this._onShowSetting.bind(this);
  }

  componentDidMount() {
    this.props.state.registerHandler(this._onChange);
  }

  _onChange() {
    this.forceUpdate();
  }

  _onShowSetting() {
    this.props.state.settingTitle = 'Settings';
    this.props.state.showSetting();
  }

  render() {
    return <div style={{textAlign:'center'}}>
             <FifteenBoard state={this.props.state} />
             <RaisedButton label="Setting"
                           onTouchTap={this._onShowSetting} />
             <SettingDialog opened={this.props.state.settingShown}
                            state={this.props.state}/>
           </div>;
  }
}

class SettingDialog extends React.Component {
  constructor() {
    super();
    this._handleRequestClose = this._handleRequestClose.bind(this);
    this._handleRequestStart = this._handleRequestStart.bind(this);
  }

  render() {
    let customActions = [
      <FlatButton label="Cancel"
                  secondary={true}
                  onTouchTap={this._handleRequestClose} />,
      <FlatButton label="Reset"
                  primary={true}
                  onTouchTap={this._handleRequestStart} />
    ];

    return (<Dialog title={this.props.state.settingTitle}
                actions={customActions}
                actionFocus="submit"
                onRequestClose={this._handleRequestClose}
                open={this.props.opened}>
              <RadioButtonGroup ref="sizeRadio" defaultSelected={String(this.props.state.n_)}>
                <RadioButton value="3"
                             label="8"
                             style={{marginBottom:16}} />
                <RadioButton value="4"
                             label="15"
                             style={{marginBottom:16}} />
                <RadioButton value="5"
                             label="24"
                             style={{marginBottom:16}} />
                <RadioButton value="6"
                             label="35"
                             style={{marginBottom:16}} />
              </RadioButtonGroup>
            </Dialog>);
  }

  _handleRequestClose() {
    this.props.state.hideSetting();
  }

  _handleRequestStart() {
    var num = Number(this.refs.sizeRadio.getSelectedValue());
    var pieceWidth = Math.floor((document.body.clientWidth - 20) / num);
    this.props.state.resetBoard(num, pieceWidth);
    this.props.state.shuffle(SHUFFLE_REPEAT);
    this.props.state.hideSetting();
  }
}

var main = function() {
  var num = 4;
  var pieceWidth = Math.floor((document.body.clientWidth - 20) / num);
  var fifteenState = new FifteenState(num, pieceWidth);
  fifteenState.shuffle(SHUFFLE_REPEAT);
  
  ReactDOM.render(<App state={fifteenState} />,
                  document.getElementById('example'));
};

main();
