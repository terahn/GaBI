import numpy as np
import librosa, librosa.display
import soundfile as sf
from placements import kick_placements, snare_placements, hat_placements

def gabi_run(input_file, drum_pack):
    # load samples
    sample, kick, snare, hat, srate = load_samples(input_file, drum_pack)

    # perform beat tracking
    tempo, drum_indices = beat_track(sample, srate)

    # perfrom any heuristics
    tempo, drum_indices = heuristics(tempo, drum_indices)

    # subdivide into quarter notes
    quarters = subdivide(drum_indices)

    # calculate drum placements
    kick_indices = kick_placements(quarters)
    snare_indices = snare_placements(quarters)
    hat_indices = hat_placements(quarters)

    # drum volumes
    kick_volume = 0.6
    snare_volume = 1.0
    hat_volume = 0.5

    kick_track = create_drum_track(sample, kick, kick_indices)
    snare_track = create_drum_track(sample, snare, snare_indices)
    hat_track = create_drum_track(sample, hat, hat_indices)

    output = sample + (kick_volume * kick_track) + (snare_volume * snare_track) + (hat_volume * hat_track)

    output_file_name = input_file + '-output.wav'
    sf.write('../output/' + output_file_name, sample + output, srate, 'PCM_24')
    print('Output file ' + output_file_name + ' can be found in the output folder')

# load the the input and drum samples
# Input:
# sample_name: string - the name of the input file
# drum_pack: int - a number corresponding to a set of drum samples (ex. kick1, snare1, hat1)
def load_samples(sample_name, drum_pack):
    x, srate = librosa.load('../samples/' + sample_name + '.wav')

    # load drum samples
    kick, sr = librosa.load('../samples/drums/kicks/kick{0}.wav'.format(drum_pack))
    snare, sr = librosa.load('../samples/drums/snares/snare{0}.wav'.format(drum_pack))
    hat, sr = librosa.load('../samples/drums/hats/hat{0}.wav'.format(drum_pack))

    return x, kick, snare, hat, srate

# perform beat tracking algorithm
# Input:
# sample: the input sample
def beat_track(sample, sr=44100):
    tempo, drum_indices = librosa.beat.beat_track(sample, sr=sr, units='samples')
    print('Estimated Tempo: ', tempo)
    return tempo, drum_indices

# any heuristics to improve the drum indices
# Input:
# tempo: the detected tempo of the input sample
# drum_indices: list of detected beat indices
def heuristics(tempo, drum_indices):
    new_indices = []
    # if tempo > 125, half speed it (maybe a good idea?)
    # if tempo > 125:
    #     drum_indices = [value for (i, value) in enumerate(drum_indices) if i % 2 == 0]

    if tempo < 60:
        for i in range(len(drum_indices) - 1):
            new_indices.append(np.linspace(drum_indices[i], drum_indices[i + 1], 2, endpoint=False).tolist())

    # flatten array if necessary
    new_indices = [item for sublist in new_indices for item in sublist]

    # new_indices will be empty if no heuristics have been performed, so return original drum_indices
    if len(new_indices) > 0:
        return tempo, new_indices
    else:
        return tempo, drum_indices

# subdivide drum indices into quarter notes (or other notes)
# Input:
# drum_indices: list of detected beat indices
def subdivide(drum_indices):
    print(drum_indices)
    quarters = []

    if drum_indices[0] > 10000:
        quarters.append(np.linspace(0, drum_indices[0], 4, endpoint=False).tolist())

    for i in range(len(drum_indices) - 1):
        quarters.append(np.linspace(drum_indices[i], drum_indices[i + 1], 4, endpoint=False).tolist())
    quarters = [item for sublist in quarters for item in sublist]

    return quarters

def create_drum_track(x, drum_sample, placements):
    # this will be the track that we add the kicks to
    track = np.zeros(len(x))
    for i in placements:
        index = int(i)
        try: # REMOVE THIS ONCE FIXED
            track[index:index+len(drum_sample)] = drum_sample
        except:
            continue
    return track

gabi_run('test', 2)