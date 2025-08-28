# -*- coding: utf-8 -*-
"""A simple sudoku solver

Created on 2025.08.28
@author: Widmo
"""


def InvalidBoard(ValueError):
    pass


def main():
    # s = Solver()
    s = Solver([[8, 0, 0, 1, 0, 9, 0, 4, 7],
                [1, 0, 4, 5, 8, 0, 0, 9, 0],
                [5, 0, 0, 4, 2, 3, 0, 0, 1],
                [0, 8, 3, 0, 0, 0, 9, 6, 0],
                [6, 0, 0, 0, 9, 8, 0, 7, 0],
                [0, 0, 7, 0, 0, 2, 0, 0, 4],
                [7, 0, 0, 2, 3, 5, 0, 0, 0],
                [0, 2, 0, 9, 1, 0, 0, 0, 8],
                [4, 0, 0, 8, 0, 6, 0, 2, 0]])

    # s.populate_board()
    print(s)

    print(repr(s))
    print()
    print(s.initialize_wave_function())




class Solver(object):
    board: list[list[int]]
    size = 9

    corner = "+"
    v_edge = "¦"
    h_edge = "--"
    cursor = ">"


    def __init__(self, board: list[list[int]]=None):
        # TODO: wrap the list mess in a class
        if board is None:
            board = []

            for x in range(self.size):
                column = []
                for y in range(self.size):
                    column.append(0)
                board.append(column)
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
                    cell = self.board[x][y]
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


    def initialize_wave_function(self) -> list[list[list[int]] | None]:
        # TODO: wrap the list mess in a class x2
        wave = []

        for x in range(self.size):
            column = []

            for y in range(self.size):
                cell = self.board[x][y]

                if cell > 0:
                    # cell is occupied
                    column.append(None)
                    continue

                possibilities = self.get_valid_values(x, y)

                # sanity check
                if len(possibilities) == 0:
                    raise InvalidBoard(f"Grid position {x}, {y} has no valid value")

                column.append(possibilities)

            wave.append(column)

        # TODO: add a check for a solved board
        return wave


    def get_valid_values(self, x: int, y: int):
        possibilities = []
        for n in range(1, self.size+1):
            if n in self.get_row(y):
                continue
            if n in self.get_column(x):
                continue
            if n in self.get_box(x // 3, y // 3):
                continue

            possibilities.append(n)

        return possibilities


    def partial_collapse(self, wave: list[list[list[int]] | None]) -> list[list[list[int]] | None]:
        # TODO: wrap the list mess in a class x3
        raise NotImplementedError


    def populate_board(self):
        # allowing "0" and " " as delete
        allowed_values = ("", ".", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

        cell_count = self.size ** 2
        c = 0
        while c < cell_count:
            y = c // self.size
            x = c % self.size

            cell = self.board[x][y]
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
                    self.board[x][y] = int(choice)
            c += 1

    def get_column(self, column: int) -> list[int]:
        return self.board[column]


    def get_row(self, row: int) -> list[int]:
        return [self.board[column][row] for column in range(self.size)]

    def get_box(self, x: int, y: int) -> list[int]:
        box = []
        for i in range(3*x, 3*x + 3):
            for j in range(3*y, 3*y + 3):
                # print(f"{i}, {j}")
                box.append(self.board[i][j])
        return box


    def _make_line(self):
        result = self.corner
        for x in range(self.size):
            result += self.h_edge
            if (x + 1) % 3 == 0:
                result += self.corner
        return result


def get_choice(allowed_values: list, prompt: str="> ") -> str:
    while True:
        raw_in = input(prompt)

        if raw_in in allowed_values:
            return raw_in
        else:
            continue


if __name__ == "__main__":
    main()
