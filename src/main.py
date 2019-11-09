import numpy as np
import librosa, librosa.display
import soundfile as sf
from placements import kick_placements, snare_placements, hat_placements

# load instrumental
input_file = '89_C_GlowingGuitar_SP'
x, srate = librosa.load('../samples/' + input_file + '.wav')

# tried to pick drum samples that would go together.. so kick1, snare1, hat1 should sound good together
drum_pack = 1

# load drum samples
kick, sr = librosa.load('../samples/drums/kicks/kick{0}.wav'.format(drum_pack))
snare, sr = librosa.load('../samples/drums/snares/snare{0}.wav'.format(drum_pack))
hat, sr = librosa.load('../samples/drums/hats/hat{0}.wav'.format(drum_pack))

# perform beat tracking alg
tempo, beat_times = librosa.beat.beat_track(x, sr=sr, units='samples')

# convert seconds to frames
drum_indices = beat_times

# TESTING
quarters = []
for i in range(len(drum_indices) - 1):
    quarters.append(np.linspace(drum_indices[i], drum_indices[i + 1], 4, endpoint=False).tolist())
quarters = [item for sublist in quarters for item in sublist]
print(quarters)
print(drum_indices)

# calculate drum placements
kick_indices = kick_placements(quarters)
snare_indices = snare_placements(quarters)
hat_indices = hat_placements(quarters)

# drum volumes
kick_volume = 0.6
snare_volume = 1.0
hat_volume = 0.5

# this will be the track that we add the kicks to
kick_track = np.zeros(len(x))
for i in kick_indices:
    index = int(i)
    try: # REMOVE THIS ONCE FIXED
        kick_track[index:index+len(kick)] = kick
    except:
        continue

# this will be the track that we add the snares to
snare_track = np.zeros(len(x))
for i in snare_indices:
    index = int(i)
    try: # REMOVE THIS ONCE FIXED
        snare_track[index:index+len(snare)] = snare
    except:
        continue

# this will be the track that we add the hats to
hat_track = np.zeros(len(x))
for i in hat_indices:
    index = int(i)
    try: # REMOVE THIS ONCE FIXED
        hat_track[index:index+len(hat)] = hat
    except:
        continue

output = x + (kick_volume * kick_track) + (snare_volume * snare_track) + (hat_volume * hat_track)

sf.write('../output/output.wav', x + output, srate, 'PCM_24')