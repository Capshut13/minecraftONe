"""Random terrain and tree generation.

Pure Python (no Ursina) so it can be tested without opening a window.
`generate()` returns a dict mapping integer cells (x, y, z) to block types.
"""

import random

GRASS = 'grass'
DIRT = 'dirt'
WOOD = 'wood'
LEAVES = 'leaves'

BLOCK_TYPES = (GRASS, DIRT, WOOD, LEAVES)

SPAWN_CLEARING = 4   # no wood or leaves within this many blocks of the centre


def _height_map(size, rng, max_height):
    """Random column heights, smoothed so the land forms gentle hills."""
    heights = [[rng.randint(1, max_height) for _ in range(size)] for _ in range(size)]
    for _ in range(3):
        smoothed = [[0] * size for _ in range(size)]
        for x in range(size):
            for z in range(size):
                neighbors = [
                    heights[nx][nz]
                    for nx in range(max(0, x - 1), min(size, x + 2))
                    for nz in range(max(0, z - 1), min(size, z + 2))
                ]
                smoothed[x][z] = round(sum(neighbors) / len(neighbors))
        heights = smoothed
    return heights


def _place_trees(cells, heights, size, rng, count, keep_clear):
    """Drop simple trees (trunk + leaf canopy) onto the terrain."""
    for _ in range(count):
        x = rng.randrange(2, size - 2)
        z = rng.randrange(2, size - 2)
        if keep_clear(x, z):
            continue

        base = heights[x][z]          # first empty cell above the grass
        trunk = rng.randint(3, 4)
        top = base + trunk - 1

        for y in range(base, base + trunk):
            cells[(x, y, z)] = WOOD

        for y in range(top - 1, top + 2):
            # The top layer is a plus shape; lower layers are a full 5x5 square
            radius = 1 if y == top + 1 else 2
            for dx in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    if y == top + 1 and abs(dx) == 1 and abs(dz) == 1:
                        continue
                    cell = (x + dx, y, z + dz)
                    if not (0 <= cell[0] < size and 0 <= cell[2] < size):
                        continue
                    if cell not in cells:
                        cells[cell] = LEAVES


def generate(size=32, seed=None, max_height=4, trees=None):
    """Build a `size` x `size` world. The same seed always gives the same world."""
    rng = random.Random(seed)
    heights = _height_map(size, rng, max_height)

    cells = {}
    for x in range(size):
        for z in range(size):
            h = heights[x][z]
            for y in range(h):
                cells[(x, y, z)] = GRASS if y == h - 1 else DIRT

    # Keep the spawn area clear of trees so the player does not start inside one.
    # The margin is larger than the spawn clearing because canopies reach 2 blocks
    # out from the trunk.
    centre = size // 2

    def keep_clear(x, z):
        return abs(x - centre) < SPAWN_CLEARING + 2 and abs(z - centre) < SPAWN_CLEARING + 2

    if trees is None:
        trees = size * size // 25
    _place_trees(cells, heights, size, rng, trees, keep_clear)
    return cells


def spawn_height(cells, size):
    """Y value of the top block in the centre column (where the player spawns)."""
    centre = size // 2
    column = [y for (x, y, z) in cells if x == centre and z == centre]
    return max(column) if column else 0
