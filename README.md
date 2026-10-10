# minecraftONe

A small Minecraft-style block-building demo written in Python with the [Ursina](https://www.ursinaengine.org/) game engine. Every run generates a new world with hills, grass, dirt, and trees. Walk around, place blocks, and break them.

## Requirements

- Python 3.10 or newer (tested with Python 3.13 on Windows 11)
- Ursina 8.3.0 (listed in `requirements.txt`)

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python minecraft.py
```

A window opens with the mouse locked to the camera. The console prints the world seed.

## Controls

| Input | Action |
| --- | --- |
| `W` `A` `S` `D` | Move |
| `Space` | Jump |
| Mouse | Look around |
| Left click | Remove the block you are pointing at |
| Right click | Place the selected block on the face you are pointing at |
| `1` `2` `3` `4` | Select grass, dirt, wood, or leaves |
| `Esc` | Quit |

The block you are pointing at turns lime. The bottom-left text shows which block type is selected.

## Block types

| Key | Block | Where it appears |
| --- | --- | --- |
| 1 | Grass | Top layer of every column of terrain |
| 2 | Dirt | Layers under the grass |
| 3 | Wood | Tree trunks |
| 4 | Leaves | Tree canopies |

## Configuration

Edit the constants at the top of `minecraft.py`:

- `WORLD_SIZE`: width and depth of the world in blocks (default 32).
- `SEED`: set to an integer to get the same world every run. `None` picks a random seed each time.

## Project layout

| File | Purpose |
| --- | --- |
| `minecraft.py` | The game: window, block entities, player, hotbar, and input |
| `world_gen.py` | Terrain and tree generation. No Ursina dependency |
| `board.py` | Block data, neighbor and visibility rules, placement checks. No Ursina dependency |
| `test_board.py` | Unit tests for `board.py` |
| `test_world_gen.py` | Unit tests for `world_gen.py` |
| `requirements.txt` | Python dependencies |
| `PRD.md` | Product requirements document |

## Tests

```bash
python -m unittest test_board test_world_gen -v
```

The tests cover placement and removal rules, visibility, deterministic world generation from a seed, grass on top of every column, trees staying inside the world and out of the spawn area, and spawn height.

## How it works

- **Terrain.** Each column gets a random height from 1 to 4, smoothed over three passes so the land forms gentle hills. The top block of each column is grass and the blocks under it are dirt.
- **Trees.** Trees are placed at random spots away from the spawn area. Each has a 3–4 block wood trunk and a leaf canopy.
- **Coordinates.** The world is a grid of integer cells. Each block is centered on its cell, so the top surface of a height-1 column sits at `y = 0.5`.
- **Data and entities.** Every block lives in `Board` as data. Only visible blocks (those with at least one open face) get a Ursina entity. Removing or placing a block updates the entities next to it, so buried blocks appear when you dig out their neighbors.
- **Placement.** Right-click places at `cell + face normal`. Nothing happens if that cell is filled or if the player is standing in it.
- **Respawn.** Falling below `y = -20` respawns the player above the middle of the terrain.

## Troubleshooting

- **Frame rate is low.** Each visible block is a separate Ursina entity. Lower `WORLD_SIZE` to make the world smaller.
- **`AttributeError: module 'ursina.color' has no attribute 'color'`**: an old bug. Use `color.hsv(hue, saturation, value)` instead, as the current code does.
