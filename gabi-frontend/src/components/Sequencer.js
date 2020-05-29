import React from 'react';
import './Sequencer.css';

import SequencerRow from './SequencerRow';

class Sequencer extends React.Component {
    render = () => {
        return(
        <div className='seq'>
            <SequencerRow name="HI-HAT" length={16}></SequencerRow>
            <SequencerRow name="SNARE" length={16}></SequencerRow>
            <SequencerRow name="KICK" length={16}></SequencerRow>
        </div>
        );
    }
}

export default Sequencer;