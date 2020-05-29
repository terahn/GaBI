import React from 'react';
import './SequencerButton.css';

class SequencerButton extends React.Component {

    toggle = () => {
        this.props.onChange(this.props.index)
    }

    render = () => {
        return(
            <div className={this.props.on ? 'seq-button on' : 'seq-button off'} onClick={this.toggle}></div>
        );
    }
}

export default SequencerButton;