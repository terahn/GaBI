import React from 'react';
import './SequencerRow.css';

import SequencerButton from './SequencerButton.js';

class SequencerRow extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            activations: new Array(this.props.length).fill(false)
        }
    }

    toggleButton = (key) => {
        this.setState({
            activations: this.state.activations.map((item, index) => (index === key ? !item : item))
        })
    }

    render = () => {
        return(
            <div className='seq-row'>
                <div className='rowName'>{this.props.name}</div>
                {this.state.activations.map((x, index) => (
                    <SequencerButton key={index} index={index} on={x} onChange={this.toggleButton}/>
                    ))}
            </div>
        )
    }
}

export default SequencerRow;