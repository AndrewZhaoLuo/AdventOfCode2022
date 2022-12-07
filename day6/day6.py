import numpy as np
from typing import * 

TEST_FILE = "day6/test_input.txt"
INPUT_FILE = "day6/input.txt"

def read_stuff(filename) -> List[np.ndarray]:
    signals = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            signals.append(np.array([ord(c) for c in line]))
    return signals



if __name__ == "__main__":
    signals = read_stuff(INPUT_FILE)
    print("PART1:")
    for signum, signal in enumerate(signals):
        accumulator = signal == signal

        # first 3 places are impossible
        accumulator[:3] = False
        for i in range(4):
            for j in range(i + 1, 4):
                shift_signal1 = np.roll(signal, i)
                shift_signal2 = np.roll(signal, j)
                accumulator = accumulator & (shift_signal1 != shift_signal2)

        print(f"signal {signum}: {accumulator.argmax() + 1}")

    print("PART2:")
    # part 2
    for signum, signal in enumerate(signals):
        accumulator = signal == signal

        # first 13 places are impossible
        accumulator[:13] = False
        for i in range(14):
            for j in range(i + 1, 14):
                shift_signal1 = np.roll(signal, i)
                shift_signal2 = np.roll(signal, j)
                accumulator = accumulator & (shift_signal1 != shift_signal2)

        print(f"signal {signum}: {accumulator.argmax() + 1}")
