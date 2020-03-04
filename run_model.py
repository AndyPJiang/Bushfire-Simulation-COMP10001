from reference import check_ignition

def create_bgrid(f_grid, burn_seeds):

    ''' creates a b_grid from current fuel load and the cells that are
    currently burning, in order to call check_ignition fucntion '''

    b_grid = []
    for num in range(len(f_grid)):
        line = []
        for num2 in range(len(f_grid)):
            if (num, num2) in burn_seeds:
                line.append(True)
            else:
                line.append(False)
        b_grid.append(line)

    return b_grid


def next_time(f_grid, h_grid, i_threshold, w_direction, burn_seeds,
              burnt_seeds):

    ''' takes in arguments of grid of current fuel load, height grid,
    ignition threshold, wind direction, coordinates of all currently
    burning cells, and an empty list that will contain all burnt cells.
    This function returns the fuel load and all the cells that are
    burning at time t+1 '''

    b_grid = create_bgrid(f_grid, burn_seeds)

    new_burn_seeds = []  # newly burning cells

    for i in range(len(f_grid)):
        for j in range(len(f_grid)):
            if (i, j) not in burn_seeds:
                if check_ignition(b_grid, f_grid, h_grid, i_threshold,
                                  w_direction, i, j) is True:
                    new_burn_seeds.append((i, j))

    for item in burn_seeds:  # increment fuel load of burning cells
        f_grid[item[0]][item[1]] -= 1
        if f_grid[item[0]][item[1]] == 0:
            burnt_seeds.add(item)

    burn_seeds = list(set(burn_seeds).difference(burnt_seeds))
    burn_seeds += new_burn_seeds

    if len(burn_seeds) == 0:   # an indication when no more cells are burning
        return None, None

    return f_grid, burn_seeds


def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):

    ''' takes in arguments of grid of current fuel load, height grid,
    ignition threshold, wind direction and coordinates of all currently
    burning cells. Returns the final state of the landscape once no more
    cells are burning, and the number of cells being burnt by continuously
    running the next_time function until fire stops '''

    # remove any cells from burn_seeds that have initial zero fuel load
    zero_fuel_cells=set()
    for seed in burn_seeds:
        if f_grid[seed[0]][seed[1]]==0:
            zero_fuel_cells.add(seed)
    burn_seeds=list(set(burn_seeds).difference(zero_fuel_cells))

    count=0  # number of burnt cells

    while True:
        burnt_seeds = set()
        cur=(f_grid, burn_seeds)
        (f_grid, burn_seeds) = next_time(f_grid, h_grid, i_threshold,
                                         w_direction, burn_seeds, burnt_seeds)
        count+=len(burnt_seeds)

        # return f_grid and count when fire has stopped
        if (f_grid, burn_seeds) == (None, None):
            return cur[0], count
