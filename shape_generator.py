# -*- coding: utf-8 -*-
"""Messing around

Created on 2025.09.18
@author: jakub.mnn
"""


import math as m


full_cell0  = "██"
full_cell1  = "▓▓"
empty_cell0 = "--"
empty_cell1 = "  "


def main():
    center_offset = True
    radius = 5

    draw(generate_circle(radius, center_offset))
    draw(generate_line(17, 23))


def generate_line(dx: int, dy: int) -> list[list[bool]]:
    """Create a 2D list of booleans representing a line.

    result format:
        cell = result[x][y]
    """
    width  = dx+1
    height = dy+1

    length = m.sqrt(dx**2 + dy**2)
    direction = (dx/length, dy/length)

    grid = []
    for x in range(width):
        column = []
        for y in range(height):
            column.append(False)
        grid.append(column)

    for t in range(m.floor(length)):
        x = direction[0] * t
        y = direction[1] * t

        # check nearest cells, get their distance, choose the smallest
        # -1, -1
        distances = [None, None, None, None]
        newx, newy = round(x-1), round(y-1)
        distance = m.sqrt((x-newx)**2 + (y-newy)**2)


        grid[x][y] = True

    return grid


def generate_circle(radius: float, center_offset: bool=True) -> list[list[bool]]:
    """Create a 2D list of booleans representing a circle.

    center_offset specifies whether to use a 2x2 center (1x1 otherwise)

    result format:
        cell = result[x][y]
    """
    width  = 2 * m.ceil(radius) + 1 - center_offset
    height = 2 * m.ceil(radius) + 1 - center_offset


    grid = []
    for x in range(width):
        column = []
        for y in range(height):
            offset = m.ceil(radius)
            x_offset = x - offset + 0.5*center_offset
            y_offset = y - offset + 0.5*center_offset

            cell = is_inside_circle(x_offset, y_offset, radius)
            column.append(cell)

        grid.append(column)

    return grid


def is_inside_circle(x: int, y: int, radius: float):
    if m.sqrt(x**2 + y**2) <= radius:
        return True
    else:
        return False


def draw(data: list[list[bool]]) -> None:
    """Print a picture to the console based on provided data.

    cell = data[x][y]
    """
    width = len(data)
    height = len(data[0])

    result = ""
    for y in range(height):
        line = ""
        for x in range(width):
            if data[x][y]:
                if (x+y) % 2 == 0:
                    line += full_cell0
                else:
                    line += full_cell1
            else:
                if (x+y) % 2 == 0:
                    line += empty_cell0
                else:
                    line += empty_cell1
        result += line + "\n"
    print(result)


if __name__ == "__main__":
    main()
