import numpy as np
from typing import * 

"""
Tree problem so lol, no numpy today
"""

TEST_FILE = "day7/test_input.txt"
INPUT_FILE = "day7/input.txt"

class File:
    def __init__(self, name:str, size:int) -> None:
        self.name = name 
        self.size = size 

    def __str__(self) -> str:
        return f"- FILE: {self.name} {self.size}"

class Directory: 
    def __init__(self, name: str, parent: Optional["Directory"]) -> None:
        self.name = name 
        self.parent = parent 
        self.files: Dict[str, File] = {}
        self.dirs: Dict[str, "Directory"] = {}

    def add_link(self, link: Union[File, "Directory"]):
        if isinstance(link, File):
            if link.name not in self.files:
                self.files[link.name] = link
            else:
                raise ValueError()
        if isinstance(link, Directory):
            if link.name not in self.dirs:
                self.dirs[link.name] = link
            else:
                raise ValueError()

    def cd(self, name: str) -> "Directory":
        if name == '..':
            if self.parent is None:
                raise ValueError()
            return self.parent
        if name not in self.dirs:
            raise ValueError()
        return self.dirs[name]

    def __str__(self) -> str:
        strs = [f"DIRS: {self.name}"]
        for k in sorted(self.dirs.keys()):
            strs.append(f" - {k}")
        strs.append(f"FILES")
        for k, v in sorted(self.files.items()):
            strs.append(f" - {k} ({v})")
        return '\n'.join(strs)

def read_stuff(filename) -> List[np.ndarray]:
    start_dir = Directory('/', None)
    cur_dir = start_dir

    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = lines[1:] # always starts with $ cd /
        for line in lines:
            line = line.strip()
            if line.startswith('$'):
                if line[2:4] == 'cd':
                    next_dir = line[5:]
                    cur_dir = cur_dir.cd(next_dir)
            else:
                size_type, name = line.split(' ')
                # list dir
                if size_type != 'dir':
                    size = int(size_type)
                    link = File(name, size)
                else:
                    link = Directory(name, cur_dir)
                cur_dir.add_link(link)
    return start_dir

def part1_calculation(cur_dir: Directory, answer_dict: Dict[Directory, int]):
    total_size = 0
    for dir in cur_dir.dirs.values():
        part1_calculation(dir, answer_dict)
        total_size += answer_dict[dir]
    
    for file in cur_dir.files.values():
        total_size += file.size

    answer_dict[cur_dir] = total_size
    
if __name__ == "__main__":
    # part 1
    root_dir = read_stuff(INPUT_FILE)
    p1 = {}
    part1_calculation(root_dir, p1)
    p1_ans = 0 
    for k, v in p1.items():
        if v <= 100000:
            p1_ans += v 
    print(p1_ans)

    # part 2
    unused_space = 70000000 - p1[root_dir]
    wanted_space = 30000000 - unused_space

    p1_sorted = sorted(p1.items(), key=lambda x: x[1])
    for dir, size in p1_sorted:
        if size >= wanted_space:
            print(size)
            break
