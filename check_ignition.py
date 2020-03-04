def adjacent_cell(f_grid, w_direction, i, j):

    '''takes in arguments of a grid of the current fuel load , wind direction
    and the coordinates i and j of a cell. Returns a set of all adjacent cells
    of the cell with coordinates(i, j), including the cells in range due to
    the wind direction '''

    adjacent_cells_ind = [(i - 1, j - 1), (i + 1, j + 1), (i - 1, j + 1),
        (i + 1, j - 1), (i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)]

    adjacent_cells = set()  # set of all adjacent cells

    for x_ind, y_ind in adjacent_cells_ind:
        if x_ind in range(len(f_grid)) and y_ind in range(len(f_grid)):
            adjacent_cells.add((x_ind, y_ind))


    # find adjacent cells due to wind direction

    if w_direction is not None:
        wind_dict={'N': [(i - 2, j - 1), (i - 2, j), (i - 2, j + 1)],
                   'S': [(i + 2, j - 1), (i + 2, j), (i + 2, j + 1)],
                   'E': [(i - 1, j + 2), (i, j + 2), (i + 1, j + 2)],
                   'W': [(i - 1, j - 2), (i, j - 2), (i + 1, j - 2)],
                   'SW': [(i + 1, j - 2), (i + 2, j - 2), (i + 2, j - 1)],
                   'NW': [(i - 1, j - 2), (i - 2, j - 2), (i - 2, j - 1)],
                   'SE': [(i + 1, j + 2), (i + 2, j + 2), (i + 2, j + 1)],
                   'NE': [(i - 1, j + 2), (i - 2, j + 2), (i - 2, j + 1)]}

        for cell1, cell2 in wind_dict[w_direction]:
            if cell1 in range(len(f_grid)) and cell2 in range(len(f_grid)):
                adjacent_cells.add((cell1, cell2))

    return adjacent_cells


def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):

    ''' takes in arguments of the burning state, grid of current fuel load,
    height grid, ignition threshold, wind direction and coordinates of a
    cell i and j. Checks if the cell (i,j) will catch fire in time t+1 as
    per the states of its adjacent cells. It will catch fire if the ignition
    factor is greater than or equal to the ignition threshold '''

    # if fuel load is zero, the cell cannot burn
    if f_grid[i][j]==0:
        return False

    ignition_factor=0

    # check if adjacent cells are burning, and increment ignition_factor
    # according to the height

    for num1, num2 in adjacent_cell(f_grid, w_direction, i, j):
        if b_grid[num1][num2] is True:
            if h_grid[num1][num2] > h_grid[i][j]:
                ignition_factor += 0.5
            elif h_grid[num1][num2] < h_grid[i][j]:
                ignition_factor += 2
            else:
                ignition_factor += 1

    return ignition_factor >= i_threshold
