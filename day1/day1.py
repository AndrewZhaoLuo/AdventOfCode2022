import numpy as np

TEST_FILE = "day1/test_input.txt"
INPUT_FILE = "day1/input.txt"

def read_stuff(filename) -> np.ndarray:
    elf_to_calories = []
    max_length = 0

    with open(filename, 'r') as f:
        lines = f.readlines()
        lines.append('\n')
        cur_elf = []
        for line in lines:
            line = line.strip()
            if line == '':
                elf_to_calories.append(cur_elf)
                max_length = max(max_length, len(cur_elf))
                cur_elf = []
            else:
                cur_elf.append(int(line))

    for i, calories in enumerate(elf_to_calories):
        arr = np.array(calories)
        pad_length = max_length - arr.shape[0]
        arr = np.pad(arr, (0, pad_length), 'constant', constant_values=[0])
        elf_to_calories[i] = arr 

    results = np.vstack(elf_to_calories)
    return results 

if __name__ == "__main__":
    # part 1
    elf_to_calories = read_stuff(INPUT_FILE)
    print(elf_to_calories.sum(1).max())

    # part 2
    elf_to_total_calories = elf_to_calories.sum(1)
    elf_to_total_calories = np.sort(elf_to_total_calories)
    print(elf_to_total_calories[-3:].sum())
