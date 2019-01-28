import React, { Component } from 'react';
import './App.css';
import Countdown from 'react-countdown-now';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      up_yet: "Yes. Government is open until February 15th, 2019.",
      open_date: "February 15, 2019",
      cave_image: "https://upload.wikimedia.org/wikipedia/commons/7/7e/Miller%27s_Chapel_%289939448605%29.jpg",
      cave_attributions: "Oregon Caves from Cave Junction, USA [CC BY 2.0 (https://creativecommons.org/licenses/by/2.0)], via Wikimedia Commons",
      cave_image_page_link: "https://commons.wikimedia.org/wiki/File:Miller%27s_Chapel_(9939448605).jpg",
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
          <Countdown date={this.state.open_date} />
          <a href={this.state.cave_image_page_link} title={this.state.cave_attributions} >
            <img className="cave-image" width="512" alt={this.state.cave_attributions} src={this.state.cave_image}></img>
          </a>
        </header>
      </div>
    );
  }
}

export default App;
