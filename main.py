from sudoku_engine.board import SudokuBoard
from sudoku_engine.solver import BacktrackingSolver, FirstEmptySelector, MRVSelector
from sudoku import Sudoku
from sudoku_engine.utils import load_euler96_sudokus_as_boards

if __name__ == "__main__":

    boards = load_euler96_sudokus_as_boards("./sudoku.txt")


    # puzzle = Sudoku(3, seed=13).difficulty(0.8)
    # sudoku = SudokuBoard(grid=puzzle.board)
    solver = BacktrackingSolver(
        boards[49],
        selector=MRVSelector(),
        # selector=FirstEmptySelector(),
        collect_metrics=True
    )
    solver.solve()
    # print(solver.board)
    print(solver.get_metrics())
    # solutions = solver.count_solutions(max_solutions=10000)
    # print(solutions)