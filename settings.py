GRID_SIZE = 108
GRID = [756, 756]

RB_START_ENERGY = 1000
FX_START_ENERGY = 5000

# transformation factor - migration
h = 0.5 * GRID[1]
w = 0.5 * GRID[0]
Tr = (h / ((h**2 + w**2)**0.5))
