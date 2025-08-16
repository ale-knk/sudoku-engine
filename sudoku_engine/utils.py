from pathlib import Path
from typing import List
from .board import SudokuBoard

def load_euler96_sudokus_as_boards(path: str) -> List[SudokuBoard]:
    """
    Load sudokus from Project Euler #96 text file.
    Returns a list of SudokuBoard objects (0 = empty).
    """
    boards = []
    lines = Path(path).read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Grid"):
            grid = []
            for j in range(1, 10):
                row = [int(ch) for ch in lines[i + j].strip()]
                grid.append(row)
            boards.append(SudokuBoard(grid=grid))  # 👈 clave aquí
            i += 10
        else:
            i += 1
    return boards
