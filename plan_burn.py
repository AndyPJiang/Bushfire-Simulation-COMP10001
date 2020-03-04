from hidden import check_ignition, update_state, run_model

def plan_burn(f_grid, h_grid, i_threshold, town_cell):

    ''' takes in arguments of the fuel load grid, height grid,
    ignition threshold and coordinates of the town cell, and returns
    the optimal/safest cell(s) to carry out a prescribed burn on. The
    optimal cell(s) are the cells where there is the least chance of
    the town catching fire during a bushfire after a prescribed burn is
    carried out on that cell '''


    # create a list of all valid cells
    valid_cells=[]
    for i in range(len(f_grid)):
        for j in range(len(f_grid)):
            if (i, j) != town_cell and f_grid[i][j] != 0:
                pres_burn = run_model(f_grid, h_grid, i_threshold * 2, None,
                                     [(i, j)])
                if pres_burn[0][town_cell[0]][town_cell[1]] != 0:
                    valid_cells.append((i, j))


    wind_directions = ['N', 'S', 'E', 'W', 'SW', 'SE', 'NE', 'NW', None]
    scores={}  # keep count of scores of valid cells


    # find the score for each valid cell
    for cell in valid_cells:
        unsafe_scenes=0
        tot_scenes=0
        aftermath = run_model(f_grid, h_grid, i_threshold * 2, None, [cell])
        for num in range(len(f_grid)):
            for num2 in range(len(f_grid)):
                if (num, num2) != town_cell and aftermath[0][num][num2]!=0:
                    tot_scenes+=9
                    for item in wind_directions:
                        result = run_model(aftermath[0], h_grid, i_threshold,
                                           item, [(num, num2)])
                        if result[0][town_cell[0]][town_cell[1]] == 0:
                            unsafe_scenes+=1
        scores[cell] = unsafe_scenes / tot_scenes


    # find the cells with the lowest ratio of unsafe scenarios(lowest score)
    optimal_cells=[]
    safest = min(scores.values())
    for key in scores.keys():
        if scores[key]==safest:
            optimal_cells.append(key)

    return sorted(optimal_cells)
