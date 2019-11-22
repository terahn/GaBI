from itertools import cycle, islice

# Pattern
pattern = [
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], # KICK 
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], # SNARE
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # HATS
]

def kick_placements(indices):
    kick_pattern = list(islice(cycle(pattern[0]), len(indices)))
    kick_placements = [indices[i] for i in range(len(indices)) if kick_pattern[i] == 1]
    return kick_placements

def snare_placements(indices):
    snare_pattern = list(islice(cycle(pattern[1]), len(indices)))
    snare_placements = [indices[i] for i in range(len(indices)) if snare_pattern[i] == 1]
    return snare_placements

def hat_placements(indices):
    hat_pattern = list(islice(cycle(pattern[2]), len(indices)))
    hat_placements = [indices[i] for i in range(len(indices)) if hat_pattern[i] == 1]
    return hat_placements