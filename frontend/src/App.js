import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      up_yet: "No."
    }
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>
            Is the government up yet?
          </p>
          <p>
            {this.state.up_yet}
          </p>
        </header>
      </div>
    );
  }
}

export default App;
