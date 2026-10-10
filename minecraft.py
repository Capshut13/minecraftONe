import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import world_gen
from board import Board, cell_of, neighbours
from world_gen import BLOCK_TYPES, GRASS, DIRT, WOOD, LEAVES

WORLD_SIZE = 32        # the world is WORLD_SIZE x WORLD_SIZE columns
SEED = None            # set to an int to get the same world every run
FALL_LIMIT = -20       # below this height the player is respawned

# Tint for each block type (the cube texture is white, so the tint sets the look)
BLOCK_COLORS = {
    GRASS:  color.rgba(0.36, 0.72, 0.28),
    DIRT:   color.rgba(0.50, 0.34, 0.20),
    WOOD:   color.rgba(0.42, 0.27, 0.14),
    LEAVES: color.rgba(0.16, 0.52, 0.18),
}

# Number keys pick the block type to place: 1 = grass, 2 = dirt, ...
HOTBAR_KEYS = {str(i + 1): block_type for i, block_type in enumerate(BLOCK_TYPES)}

app = Ursina()

# Block data for the whole world: cell -> block type. Holds every block, even hidden ones.
world = Board()
# Entities for the blocks that are visible: cell -> Brick. Hidden blocks have no entity,
# which keeps the scene small.
entities = {}
selected_type = DIRT


class Brick(Entity):
    """A visible block. Clicks are forwarded to the world, which owns the data."""

    def __init__(self, cell, block_type):
        super().__init__(
            parent=scene,
            position=cell,
            model='cube',
            texture='white_cube',
            color=BLOCK_COLORS[block_type],
            collider='box',
        )
        self.cell = cell
        self.base_color = self.color

    def on_mouse_enter(self):
        self.color = color.lime

    def on_mouse_exit(self):
        self.color = self.base_color

    def input(self, key):
        # Only react when the mouse is actually over this block.
        if mouse.hovered_entity is not self:
            return
        if key == 'right mouse down':
            place_next_to(self)
        elif key == 'left mouse down':
            remove_block(self.cell)


def refresh(cell):
    """Make the entity at `cell` match the data: present only if the block is visible."""
    should_exist = cell in world and world.is_visible(cell)
    if should_exist and cell not in entities:
        entities[cell] = Brick(cell, world.get(cell))
    elif not should_exist and cell in entities:
        destroy(entities.pop(cell))


def refresh_around(cell):
    """A change at `cell` can show or hide the blocks next to it."""
    for c in [cell, *neighbours(cell)]:
        refresh(c)


def add_block(cell, block_type):
    world.add(cell, block_type)
    refresh_around(cell)


def remove_block(cell):
    if world.remove(cell) is not None:
        refresh_around(cell)


def place_next_to(brick, normal=None):
    """Place the selected block type on the face of `brick` the mouse points at."""
    normal = mouse.normal if normal is None else normal
    target = cell_of(brick.position + normal)
    if world.can_place(target, feet=player.position):
        add_block(target, selected_type)


# Build the world: generate the data, then create entities for the visible blocks.
seed = SEED if SEED is not None else random.randrange(1_000_000)
print(f"World seed: {seed}")
terrain = world_gen.generate(size=WORLD_SIZE, seed=seed)
for cell, block_type in terrain.items():
    world.add(cell, block_type)
for cell in terrain:
    refresh(cell)

# Spawn in the middle of the world, above the terrain (gravity lands the player)
spawn_top_y = world_gen.spawn_height(terrain, WORLD_SIZE)
SPAWN = (WORLD_SIZE // 2, spawn_top_y + 3, WORLD_SIZE // 2)

# Add a first-person character (WASD to move, Space to jump, Mouse to look)
player = FirstPersonController(position=SPAWN)

# Shows which block type a right-click will place
hotbar_text = Text(
    origin=(-.5, 0),
    position=window.bottom_left + Vec2(0.03, 0.05),
    scale=1.2,
)


def update_hotbar_text():
    hotbar_text.text = (
        f"Placing: {selected_type}   "
        "[1] grass  [2] dirt  [3] wood  [4] leaves"
    )


update_hotbar_text()


def update():
    # If the player falls off the world, respawn above the middle of the terrain.
    if player.y < FALL_LIMIT:
        player.position = SPAWN


def input(key):
    global selected_type
    if key == 'escape':
        application.quit()
    elif key in HOTBAR_KEYS:
        selected_type = HOTBAR_KEYS[key]
        update_hotbar_text()


app.run()
