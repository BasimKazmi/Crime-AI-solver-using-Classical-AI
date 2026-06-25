# utils.py

def matches_clues(suspect_data, clues):

    for clue, value in clues.items():

        if suspect_data.get(clue) != value:
            return False

    return True