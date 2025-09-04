# -*- coding: utf-8 -*-
"""A simple sudoku solver

Created on 2025.08.28
@author: Widmo
"""


def main():
    # b = Board()
    # b = Board([[8, 0, 0, 1, 0, 9, 0, 4, 7],
    #            [1, 0, 4, 5, 8, 0, 0, 9, 0],
    #            [5, 0, 0, 4, 2, 3, 0, 0, 1],
    #            [0, 8, 3, 0, 0, 0, 9, 6, 0],
    #            [6, 0, 0, 0, 9, 8, 0, 7, 0],
    #            [0, 0, 7, 0, 0, 2, 0, 0, 4],
    #            [7, 0, 0, 2, 3, 5, 0, 0, 0],
    #            [0, 2, 0, 9, 1, 0, 0, 0, 8],
    #            [4, 0, 0, 8, 0, 6, 0, 2, 0]])

    b = Board([[9, 0, 6, 0, 2, 0, 8, 0, 0],
               [0, 4, 0, 9, 3, 0, 0, 6, 0],
               [3, 7, 8, 0, 0, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 5, 2, 0, 9],
               [0, 0, 3, 0, 4, 0, 1, 0, 0],
               [1, 0, 5, 2, 0, 0, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 5, 2, 8],
               [0, 1, 0, 0, 8, 3, 0, 9, 0],
               [4, 0, 9, 0, 7, 0, 6, 0, 0]])

    s = Solver(b)

    # s.populate_board()
    print(s)
    print(repr(s))

    print()
    s.initialize_wave_function()
    # print(s.wave)

    print()
    s.partial_collapse()
    print(s)
    # print(s.wave)


def get_choice(allowed_values: list, prompt: str="> ") -> str:
    while True:
        raw_in = input(prompt)

        if raw_in in allowed_values:
            return raw_in
        else:
            continue


class InvalidBoard(ValueError):
    """Raised when an inconsistency in the board is detected.

    ex.: when an empty cell has no valid value
    """
    ...


class SkillIssue(ValueError):
    """Raised when the Solver can't solve a board with available algorithms."""
    ...


class Board(object):
    """Stores the value in each cell on the board."""
    board: list[list[int]]
    size: int


    def __repr__(self):
        return f"Board({repr(self.board)})"


    def __init__(self, board: list[list[int]]=None, size: int = 9):
        if board is None:
            # initialize a new board
            board = []

            for x in range(size):
                column = []
                for y in range(size):
                    column.append(0)
                board.append(column)

        self.board = board
        self.size = size


    def set_cell(self, x: int, y: int, value: int) -> None:
        """Set the value of the cell x, y to value."""
        self.board[x][y] = value


    def get_cell(self, x: int, y: int) -> int:
        """Get the value of cell x, y."""
        return self.board[x][y]


    def get_column(self, column: int) -> list[int]:
        """Get the values of cells in the given column."""
        return [cell for cell in self.board[column]]


    def get_row(self, row: int) -> [int]:
        """Get the values of cells in the given row."""
        return [self.get_cell(column, row) for column in range(self.size)]


    def get_box(self, x: int, y: int) -> list[int]:
        """Get the values of cells in the given 3x3 box."""
        box = []
        for i in range(3*x, 3*x + 3):
            for j in range(3*y, 3*y + 3):
                # print(f"{i}, {j}")
                box.append(self.board[i][j])
        return box


class WaveFunction(object):
    """Stores the possible values for each empty cell."""
    wave: list[list[list[int]] | None]
    size: int


    def __init__(self, board: Board):
        self.size = board.size
        self.initialize_wave_function(board)


    def __repr__(self):
        return f"WaveFunction({repr(self.wave)})"


    def initialize_wave_function(self, board: Board) -> None:
        """Find all possible values for each empty cell on the board."""
        # TODO: wrap the list mess in a class
        wave = []

        for x in range(self.size):
            column = []

            for y in range(self.size):
                cell = board.get_cell(x, y)

                if cell > 0:
                    # cell is occupied
                    column.append(None)
                    continue

                possibilities = self.get_valid_values(x, y, board)

                # sanity check
                if possibilities == []:
                    raise InvalidBoard(f"Grid position {x}, {y} has no valid value")

                column.append(possibilities)

            wave.append(column)

        # TODO: add a check for a solved board
        self.wave = wave


    def get_valid_values(self, x: int, y: int, board: Board) -> list[int]:
        """Get all possible values for a given cell."""
        possibilities = []
        for n in range(1, self.size+1):
            if n in board.get_row(y):
                continue
            if n in board.get_column(x):
                continue
            if n in board.get_box(x // 3, y // 3):
                continue

            possibilities.append(n)

        return possibilities


    def set_cell(self, x: int, y: int, value: list[int]) -> None:
        """Set the value of the cell x, y to value."""
        self.wave[x][y] = value


    def get_cell(self, x: int, y: int) -> list[float]:
        """Get the calculated values of cell x, y."""
        return self.wave[x][y]


    def get_column(self, column: int) -> list[int]:
        """Get the calculated values for each cell in the given column."""
        return [cell for cell in self.wave[column]]


    def get_row(self, row: int) -> list[int]:
        """Get the calculated values for each cell in the given row."""
        return [self.get_cell(column, row) for column in range(self.size)]


    def get_box(self, x: int, y: int) -> list[int]:
        """Get the calculated values for each cell in the given 3x3 box."""
        box = []
        for i in range(3*x, 3*x + 3):
            for j in range(3*y, 3*y + 3):
                # print(f"{i}, {j}")
                box.append(self.wave[i][j])
        return box


    def remove(self, x: int, y: int, index: int):
        """Remove a specific value from the given cell.

        Uses index instead of value because this function is a drop-in
        replacement for a del statement.
        """
        del self.wave[x][y][index]


class Solver(object):
    """Handles the solving."""
    board: Board
    wave:  WaveFunction
    size = 9

    corner = "+"
    v_edge = "¦"
    h_edge = "--"
    cursor = ">"


    def __init__(self, board: Board=None):
        if board is None:
            board = Board()

        else:
            # TODO: check if board is valid
            pass

        self.board = board


    def __repr__(self):
        return f"Solver({repr(self.board)})"


    def __str__(self, override: (int, int, int)=None):
        corner = self.corner
        v_edge = self.v_edge
        h_edge = self.h_edge
        h_line = self._make_line()

        if override is None:
            overwrite = False
        else:
            overwrite = True

        result = h_line + "\n"
        for y in range(self.size):
            if y > 0:
                row = "\n" + v_edge
            else:
                row = v_edge

            for x in range(self.size):
                if overwrite and (x, y) == (override[0], override[1]):
                    cell = override[2]

                else:
                    cell = self.board.get_cell(x, y)
                    if cell > 0:
                        cell = " " + str(cell)
                    else:
                        cell = "  "

                row += cell

                if (x + 1) % 3 == 0:
                    row += v_edge

            if (y + 1) % 3 == 0:
                row += "\n" + h_line
            result += row

        return result


    def initialize_wave_function(self) -> None:
        """Create a new WaveFunction."""
        self.wave = WaveFunction(self.board)


    def partial_collapse(self) -> None:
        """Use a simplified wave function collapse algorithm to fill in empty
        cells.

        Make sure the WaveFunction is initialized before calling this.
        """
        queue = []

        for x in range(self.size):
            column = self.wave.get_column(x)
            for y, cell in enumerate(column):
                if cell is None:
                    continue

                if cell == []:
                    raise InvalidBoard(f"Grid position {x}, {y} has no valid value")

                if len(cell) == 1:
                    queue.append((x, y))

        # print(stack)

        while len(queue) > 0:
            cell = queue.pop()
            self.collapse_cell(*cell, queue)


    def check_uniqueness(self, x: int, y: int) -> None:
        for value in self.wave[x][y]:
            raise NotImplementedError



    def collapse_cell(self, x: int, y: int, queue) -> None:
        """Set the value of a cell with one remaining value and update its
        neighbors.
        """
        value = self.wave.get_cell(x, y)[0]
        self.board.set_cell(x, y, value)
        self.wave.set_cell(x, y, None)

        # update column
        for j, cell in enumerate(self.wave.get_column(x)):
            if cell is None:
                continue

            for index, cell_value in enumerate(cell):

                if cell_value == value:
                    # print(f"removing {cell_value} from {x}, {j}")
                    self.wave.remove(x, j, index)
                    if len(cell) <= 1 and (x, j) not in queue:
                        queue.append((x, j))

        # update row
        for i in range(self.size):
            cell = self.wave.get_cell(i, y)

            if cell is None:
                continue

            for index, cell_value in enumerate(cell):

                if cell_value == value:
                    # print(f"removing {cell_value} from {i}, {y}")
                    self.wave.remove(i, y, index)
                    if len(cell) <= 1 and (i, y) not in queue:
                        queue.append((i, y))

        # update box
        box = []
        box_x = x // 3
        box_y = y // 3
        for i in range(3*box_x, 3*box_x + 3):
            for j in range(3*box_y, 3*box_y + 3):
                cell = self.wave.get_cell(i, j)

                if cell is None:
                    continue

                for index, cell_value in enumerate(cell):

                    if cell_value == value:
                        # print(f"removing {cell_value} from {i}, {j}")
                        self.wave.remove(i, j, index)
                        if len(cell) <= 1 and (i, j) not in queue:
                            queue.append((i, j))


    def populate_board(self):
        """Prompt the user to fill in the cells on the board.

        The board does not need to be empty.
        """
        # allowing "0" and " " as delete
        allowed_values = ("", ".", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        cell_count = self.size ** 2
        c = 0
        while c < cell_count:
            y = c // self.size
            x = c % self.size

            cell = self.board.get_cell(x, y)
            # print board with current cell highlighted
            str_cell = str(cell) if cell > 0 else " "
            print(self.__str__((x, y, self.cursor+str_cell)))

            choice = get_choice(allowed_values)

            match choice:
                case "":
                    pass
                case ".":
                    if c > 0:
                        c -= 2
                    else:
                        c = -1
                case " ":
                    self.board[x][y] = 0
                case _:
                    # 0-9 digits only (0 is clear)
                    # everything else got filtered out by get_choice()
                    self.board.set_cell(x, y, int(choice))
            c += 1

        self.wave = WaveFunction(self.board)


    def _make_line(self):
        """Creates a horizontal text line.

        Used for drawing the board in a CLI.
        """
        result = self.corner
        for x in range(self.size):
            result += self.h_edge
            if (x + 1) % 3 == 0:
                result += self.corner
        return result


if __name__ == "__main__":
    main()
