class SudokuBoard:
    def _initialize_grid(self, size: int, grid: list[list[int]] = None) -> list[list[int]]:
        if grid is None:
            return [[0] * size for _ in range(size)]
        return [[0 if cell is None else cell for cell in row] for row in grid]

    def __init__(self, size: int = 9, grid: list[list[int]] = None):
        self._size = size
        self._box_size = int(size ** 0.5)
        self._grid = self._initialize_grid(size, grid)
        self._fixed_positions = {
            (r, c)
            for r in range(size)
            for c in range(size)
            if self._grid[r][c] != 0
        }

    def get_cell(self, row: int, col: int) -> int:
        return self._grid[row][col]

    def set_cell(self, row: int, col: int, value: int):
        if (row, col) in self._fixed_positions:
            raise ValueError("Cannot modify a fixed cell.")
        if not (0 <= value <= self._size):
            raise ValueError(f"Value must be between 0 and {self._size}.")
        if value != 0 and not self.is_valid_move(row, col, value):
            raise ValueError(f"Invalid move: {value} at ({row}, {col})")
        self._grid[row][col] = value

    def is_valid_move(self, row: int, col: int, value: int) -> bool:
        # Check row
        if value in self._grid[row]:
            return False
        # Check column
        if value in (self._grid[r][col] for r in range(self._size)):
            return False
        # Check box
        start_row = (row // self._box_size) * self._box_size
        start_col = (col // self._box_size) * self._box_size
        for r in range(start_row, start_row + self._box_size):
            for c in range(start_col, start_col + self._box_size):
                if self._grid[r][c] == value:
                    return False
        return True

    def __str__(self) -> str:
        lines = []
        for r in range(self._size):
            row_str = ""
            for c in range(self._size):
                val = self._grid[r][c]
                row_str += str(val) if val != 0 else "."
                if (c + 1) % self._box_size == 0 and c != self._size - 1:
                    row_str += " | "
                else:
                    row_str += " "
            lines.append(row_str.strip())
            if (r + 1) % self._box_size == 0 and r != self._size - 1:
                lines.append("-" * (self._size * 2 + self._box_size - 1))
        return "\n".join(lines)
