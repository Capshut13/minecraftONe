# PRD: minecraftONe block-building demo

**Status:** Prototype, v0.2
**Owner:** glass418cloudy@gmail.com
**Last updated:** 2026-10-10

## 1. Summary

minecraftONe is a single-player, first-person block-building prototype in the style of Minecraft. Each run generates a random landscape of grass, dirt, trees, and leaves. The player walks on the terrain, places blocks from a small hotbar, and removes blocks. It is a starting point for experiments with voxel worlds in Python.

## 2. Goals

- Generate a new, random, playable terrain on every run (or from a fixed seed).
- Let the player place and remove blocks of several types in first person.
- Keep placement rules correct: no duplicate blocks, no blocks inside the player.
- Keep the scene responsive by only rendering blocks that can be seen.
- Keep the world logic and terrain generation testable without opening a window.

## 3. Non-goals (for this version)

- Multiplayer, saving or loading worlds.
- Textures, inventory, crafting, or more than four block types.
- Biomes, caves, water, day/night, mobs, health, or combat.
- Mobile or web builds.

## 4. Users

A developer or hobbyist who wants a small, readable starting point for a voxel-style game in Python.

## 5. Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| F1 | On start, generate a random terrain of WORLD_SIZE x WORLD_SIZE columns with hills. Each column has grass on top and dirt below. | Must |
| F2 | Generation is deterministic for a given seed. A fixed seed can be set in code. | Must |
| F3 | Trees (wood trunk and leaf canopy) are placed on the terrain, away from the spawn area. | Must |
| F4 | The player spawns above the middle of the terrain and lands on it. | Must |
| F5 | WASD moves, Space jumps, mouse looks around. | Must |
| F6 | Right-clicking places the selected block type on the face under the mouse. | Must |
| F7 | Left-clicking removes the block under the mouse. | Must |
| F8 | A new block is never placed in a cell that already has a block. | Must |
| F9 | A new block is never placed in a cell the player occupies. | Must |
| F10 | Keys 1–4 select grass, dirt, wood, or leaves. The current selection is shown on screen. | Should |
| F11 | Blocks with no open face are not rendered. They appear when a neighbor is removed. | Should |
| F12 | The block under the mouse is highlighted. | Should |
| F13 | Falling below the world respawns the player. | Should |
| F14 | `Esc` quits the game. | Should |

## 6. Non-functional requirements

- **Startup:** world generation and entity creation should finish in a few seconds on a typical PC. Not yet measured on target hardware.
- **Frame rate:** should stay playable with the default world (32 x 32). Headless measurements in development showed about 15 frames per second with software rendering; this needs measuring on a real GPU.
- **Dependencies:** Python 3.10+ and `ursina==8.3.0`, pinned in `requirements.txt`.
- **Testability:** terrain generation (`world_gen.py`) and block rules (`board.py`) have no engine dependency and are covered by unit tests.

## 7. Design

- `minecraft.py`: Ursina app, `Brick` entity, visibility tracking, hotbar, input, and player setup.
- `world_gen.py`: `generate(size, seed)` returns a dict of cell to block type. Also `spawn_height`.
- `board.py`: `Board` (cell to block type map, visibility, placement checks), `cell_of`, `neighbours`, and `overlaps_player`.
- Coordinates: integer cells; each block is centered on its cell.
- Visibility: an entity exists only for a block with at least one face next to empty space. Changes update the affected block and its six neighbors.
- Placement: target cell = `cell_of(block.position + face_normal)`. Placed only if `Board.can_place` returns true.

## 8. Success criteria

- `python minecraft.py` starts, prints a seed, and shows a terrain with grass, dirt, trees, and leaves.
- The same seed produces the same terrain (checked by unit test).
- All tests in `test_board.py` and `test_world_gen.py` pass (27 tests).
- Placing, removing, hotbar selection, and standing on the terrain all behave as described in section 5.

## 9. Open questions

- Should the player collide physically with blocks, or keep the current raycast-based movement?
- What frame rate is acceptable on the target machine, and does the default world size need to change?
- Should the world be generated in chunks so it can grow beyond a fixed size?

## 10. Milestones

1. **Done (v0.1):** Floor, first-person movement, place and remove, placement rules, tests, docs.
2. **Done (v0.2):** Random terrain, grass, dirt, wood, leaves, trees, hotbar, visibility culling, tests, docs.
3. **Next:** Measure frame rate on target hardware; decide on chunked generation.
4. **Later:** Save and load the world to a file.
