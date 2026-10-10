"""Tests for world_gen.py. Run with: python -m unittest test_world_gen"""

import unittest

from world_gen import BLOCK_TYPES, DIRT, GRASS, LEAVES, SPAWN_CLEARING, WOOD, generate, spawn_height

SIZE = 32


class GenerateTests(unittest.TestCase):
    def setUp(self):
        self.cells = generate(size=SIZE, seed=1234)

    def test_same_seed_gives_same_world(self):
        self.assertEqual(generate(size=SIZE, seed=42), generate(size=SIZE, seed=42))

    def test_different_seeds_give_different_worlds(self):
        self.assertNotEqual(generate(size=SIZE, seed=1), generate(size=SIZE, seed=2))

    def test_only_known_block_types(self):
        self.assertTrue(set(self.cells.values()) <= set(BLOCK_TYPES))

    def test_every_column_has_grass_on_top(self):
        tops = {}
        for (x, y, z), block_type in self.cells.items():
            if block_type == LEAVES or block_type == WOOD:
                continue
            tops[(x, z)] = max(tops.get((x, z), -1), y)
        for (x, z), top_y in tops.items():
            self.assertEqual(self.cells[(x, top_y, z)], GRASS)

    def test_dirt_is_below_grass(self):
        for (x, y, z), block_type in self.cells.items():
            if block_type == DIRT:
                self.assertIn((x, y + 1, z), self.cells)

    def test_terrain_covers_the_whole_grid(self):
        columns = {(x, z) for (x, _, z) in self.cells}
        self.assertEqual(len(columns), SIZE * SIZE)

    def test_contains_trees(self):
        self.assertIn(WOOD, self.cells.values())
        self.assertIn(LEAVES, self.cells.values())

    def test_everything_stays_inside_the_grid(self):
        for x, y, z in self.cells:
            self.assertTrue(0 <= x < SIZE and 0 <= z < SIZE)
            self.assertGreaterEqual(y, 0)

    def test_no_trees_in_spawn_area(self):
        centre = SIZE // 2
        for (x, y, z), block_type in self.cells.items():
            if block_type in (WOOD, LEAVES):
                self.assertFalse(abs(x - centre) < SPAWN_CLEARING and abs(z - centre) < SPAWN_CLEARING)


class SpawnHeightTests(unittest.TestCase):
    def test_returns_top_block_of_centre_column(self):
        cells = {(16, 0, 16): DIRT, (16, 1, 16): GRASS}
        self.assertEqual(spawn_height(cells, 32), 1)

    def test_empty_world_returns_zero(self):
        self.assertEqual(spawn_height({}, 32), 0)


if __name__ == '__main__':
    unittest.main()
