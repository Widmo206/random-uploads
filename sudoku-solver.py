# -*- coding: utf-8 -*-
"""A simple sudoku solver

Created on 2025.08.28
@author: Widmo
"""


def main():
    s = solver()
    print(s)

    s.populate()

    print(s)


class solver(object):
    board: list[list[int]]
    size = 9

    corner = "+"
    v_edge = "¦"
    h_edge = "--"
    cursor = ">"


    def __init__(self):
        board = []

        for x in range(self.size):
            column = []
            for y in range(self.size):
                column.append(0)
            board.append(column)

        self.board = board


    def __repr__(self):
        return repr(self.board)


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


    def populate(self):
        allowed_values = ["", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

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
                case _:
                    self.board[x][y] = int(choice)
            c += 1


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
