

WIND_DIRECTIONS = {'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', None}


def is_valid(data):
    size = len(data['f_grid'])
    if data['i_threshold'] < 1 or data['i_threshold'] > 8:
        return False
    if data['w_direction'] not in WIND_DIRECTIONS:
        return False
    for r, c in data['burn_seeds']:
        if r < 0 or r >= size or c < 0 or c >= size:
            return False
        elif data['f_grid'][r][c] < 1:
            return False
    return True


def parse_scenario(filename):
    # Read the whole file.
    with open(filename) as f:
        lines = f.readlines()[::-1]

    """Extract the size of the grid, initial fuel values for each cell in the
    grid, height values for each cell in the grid, ignition threshold, wind
    diretion, and grid locations for the cells that are initially burning.
    Format data and eturn a dictionary 
    """
    
    size = int(lines.pop())

    fuels = [list(map(int, lines.pop().split(','))) for r in range(size)]

    heights = [list(map(int, lines.pop().split(','))) for r in range(size)]

    ignition_threshold = int(lines.pop())

    wind_direction = lines.pop().strip()

    if wind_direction == 'None':
        wind_direction = None

    burning_cells = [tuple(map(int, line.split(','))) for line in lines[::-1]]


    # Validate the data and return appropriately.
    data = {
        'f_grid': fuels,
        'h_grid': heights,
        'i_threshold': ignition_threshold,
        'w_direction': wind_direction,
        'burn_seeds': burning_cells,
    }
    return data if is_valid(data) else None
