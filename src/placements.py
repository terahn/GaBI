from itertools import cycle, islice

# Pattern
pattern = [
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], # KICK 
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], # SNARE
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # HATS
]

def kick_placements(indices, pattern):
    kick_pattern = list(islice(cycle(pattern), len(indices)))
    kick_placements = [indices[i] for i in range(len(indices)) if kick_pattern[i] == True]
    return kick_placements

def snare_placements(indices, pattern):
    snare_pattern = list(islice(cycle(pattern), len(indices)))
    snare_placements = [indices[i] for i in range(len(indices)) if snare_pattern[i] == True]
    return snare_placements

def hat_placements(indices, pattern):
    hat_pattern = list(islice(cycle(pattern), len(indices)))
    hat_placements = [indices[i] for i in range(len(indices)) if hat_pattern[i] == True]
    return hat_placements