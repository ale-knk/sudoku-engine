from typing import Dict, Optional, Protocol
import time
from .board import SudokuBoard

class CellSelector(Protocol):
    def select(self, board: SudokuBoard) -> Optional[tuple[int, int]]:
        """Return coordinates of next cell to explore, or None if none available."""
        ...

class FirstEmptySelector:
    def select(self, board: SudokuBoard) -> Optional[tuple[int, int]]:
        size = board._size
        for r in range(size):
            for c in range(size):
                if board.get_cell(r, c) == 0:
                    return r, c
        return None

class MRVSelector:
    def select(self, board: SudokuBoard) -> Optional[tuple[int, int]]:
        size = board._size
        best_cell = None
        min_options = size + 1

        for r in range(size):
            for c in range(size):
                if board.get_cell(r, c) == 0:
                    options = [
                        num for num in range(1, size + 1)
                        if board.is_valid_move(r, c, num)
                    ]
                    if len(options) < min_options:
                        min_options = len(options)
                        best_cell = (r, c)
                        if min_options == 1:
                            return best_cell
        return best_cell

class BacktrackingSolver:
    def __init__(self, board: SudokuBoard, selector: CellSelector, collect_metrics: bool = False):
        self.board = board
        self.size = board._size
        self.selector = selector
        self.solutions_found = 0
        self.max_solutions = 1
        self.collect_metrics = collect_metrics

        if collect_metrics:
            self._metrics = {
                'start_time': None,
                'end_time': None,
                'total_attempts': 0,
                'valid_moves': 0,
                'backtracking_count': 0,
                'max_recursion_depth': 0,
                'current_recursion_depth': 0,
                'initial_empty_cells': sum(
                    1 for r in range(self.size) 
                    for c in range(self.size) 
                    if self.board.get_cell(r, c) == 0
                )
            }

    def _find_empty(self) -> Optional[tuple[int, int]]:
        return self.selector.select(self.board)

    def solve(self) -> bool:
        if self.collect_metrics and self._metrics['start_time'] is None:
            self._metrics['start_time'] = time.perf_counter()
            self._metrics['current_recursion_depth'] = 0

        empty = self._find_empty()
        if not empty:
            if self.collect_metrics:
                self._metrics['end_time'] = time.perf_counter()
            return True

        r, c = empty
        if self.collect_metrics:
            self._metrics['current_recursion_depth'] += 1
            self._metrics['max_recursion_depth'] = max(
                self._metrics['max_recursion_depth'],
                self._metrics['current_recursion_depth']
            )

        for num in range(1, self.size + 1):
            if self.collect_metrics:
                self._metrics['total_attempts'] += 1

            if self.board.is_valid_move(r, c, num):
                if self.collect_metrics:
                    self._metrics['valid_moves'] += 1

                self.board.set_cell(r, c, num)
                if self.solve():
                    return True

                # Backtrack
                self.board.set_cell(r, c, 0)
                if self.collect_metrics:
                    self._metrics['backtracking_count'] += 1

        if self.collect_metrics:
            self._metrics['current_recursion_depth'] -= 1
        return False

    def count_solutions(self, max_solutions: int = 2) -> int:
        self.solutions_found = 0
        self.max_solutions = max_solutions
        self._search_count()
        return self.solutions_found

    def _search_count(self):
        if self.solutions_found >= self.max_solutions:
            return

        empty = self._find_empty()
        if not empty:
            self.solutions_found += 1
            return

        r, c = empty
        for num in range(1, self.size + 1):
            if self.board.is_valid_move(r, c, num):
                self.board.set_cell(r, c, num)
                self._search_count()
                self.board.set_cell(r, c, 0)

    def get_metrics(self) -> Dict:
        if not self.collect_metrics:
            return {}

        metrics = self._metrics.copy()

        metrics.pop('start_time', None)
        metrics.pop('end_time', None)

        if self._metrics['end_time'] is not None:
            metrics['total_time'] = self._metrics['end_time'] - self._metrics['start_time']
            if self._metrics['valid_moves'] > 0:
                metrics['avg_time_per_move'] = metrics['total_time'] / self._metrics['valid_moves']

        if self._metrics['total_attempts'] > 0:
            metrics['success_rate'] = self._metrics['valid_moves'] / self._metrics['total_attempts']

        if self._metrics['initial_empty_cells'] > 0:
            metrics['avg_attempts_per_cell'] = self._metrics['total_attempts'] / self._metrics['initial_empty_cells']

        return metrics
