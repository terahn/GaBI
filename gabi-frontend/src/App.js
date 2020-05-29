import React from 'react';
import './App.css';
import Sequencer from './components/Sequencer.js'

class App extends React.Component {

  constructor(props) {
    super(props);
      this.state = {
        selectedFile: null
      }
  }

  fileUploaded = (event) => {
    console.log(event.target.files[0])
    this.setState({
      selectedFile:  event.target.files[0]
    })
  }

  generate = () => {
    console.log('Generate clicked.')
  }

  render = () => {
      return(
        <div className="App">
          <div className="upload-region">
            <label className="fileContainer button">
              UPLOAD
              <input type="file" onChange={this.fileUploaded}/>
            </label>
          </div>
          <Sequencer></Sequencer>
          <div className="generate-region">
            <button className="button" onClick={this.generate}>GENERATE</button>
          </div>
      </div>
      );
  }
}

export default App;
