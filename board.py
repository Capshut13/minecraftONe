"""Grid bookkeeping for the block world.

This module has no Ursina dependency so the placement rules can be tested
without opening a window.
"""

PLAYER_RADIUS = 0.3   # horizontal half-width of the player's body
PLAYER_HEIGHT = 2.0   # matches FirstPersonController's default height


FACE_OFFSETS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def neighbours(cell):
    """The six cells that share a face with `cell`."""
    x, y, z = cell
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in FACE_OFFSETS]


def cell_of(position):
    """Snap a world position to the integer grid cell it belongs to."""
    return tuple(int(round(c)) for c in position)


def overlaps_player(cell, feet):
    """True if a block in `cell` would intersect a player standing at `feet`."""
    cx, cy, cz = cell
    fx, fy, fz = feet
    block_half = 0.5
    horizontal = (abs(cx - fx) < block_half + PLAYER_RADIUS and
                  abs(cz - fz) < block_half + PLAYER_RADIUS)
    vertical = (cy + block_half > fy and cy - block_half < fy + PLAYER_HEIGHT)
    return horizontal and vertical


class Board:
    """Maps integer grid cells to the block objects that occupy them."""

    def __init__(self):
        self._cells = {}

    def __contains__(self, cell):
        return cell in self._cells

    def __len__(self):
        return len(self._cells)

    def get(self, cell):
        return self._cells.get(cell)

    def add(self, cell, block):
        if cell in self._cells:
            raise ValueError(f"cell {cell} is already occupied")
        self._cells[cell] = block

    def remove(self, cell):
        return self._cells.pop(cell, None)

    def is_visible(self, cell):
        """A block is visible if at least one of its six faces touches empty space."""
        return any(n not in self._cells for n in neighbours(cell))

    def can_place(self, cell, feet=None):
        """A cell is placeable if it is empty and not inside the player."""
        if cell in self._cells:
            return False
        if feet is not None and overlaps_player(cell, feet):
            return False
        return True
