import numpy as np

TEST_FILE = "day2/test_input.txt"
INPUT_FILE = "day2/input.txt"

MAP_TO_PLAY = {
    # Rock / LOSE
    "X": 0,
    "A": 0,

    # Paper / DRAW
    "Y": 1,
    "B": 1,

    # Scissors / WIN
    "Z": 2,
    "C": 2,
}

PLAY_POINT_COUNTS = [0, 3, 6]
CHOSEN_POINT_COUNTS = [1, 2, 3]

def read_stuff(filename) -> np.ndarray:
    plays = []

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            results = line.split(' ')
            plays.append(
                [MAP_TO_PLAY[results[0]], MAP_TO_PLAY[results[1]]]
            )

    return np.array(plays) 

if __name__ == "__main__":
    # part 1
    encoding = read_stuff(INPUT_FILE)
    plays = (encoding[:, 1] - encoding[:, 0] + 1) % 3
    points_from_plays = np.take(PLAY_POINT_COUNTS, plays)
    points_from_chosen = np.take(CHOSEN_POINT_COUNTS, encoding[:, 1].flatten())
    points = points_from_plays + points_from_chosen
    print(points.sum())

    # part 2 
    proper_play = (encoding[:, 1] - 1 + encoding[:, 0]) % 3
    points_from_plays = np.take(PLAY_POINT_COUNTS, encoding[:, 1])
    points_from_chosen = np.take(CHOSEN_POINT_COUNTS, proper_play)
    points = points_from_plays + points_from_chosen
    print(points.sum())