"""Tests for the grid rules in board.py. Run with: python -m unittest test_board"""

import unittest

from board import Board, cell_of, neighbours, overlaps_player


class CellOfTests(unittest.TestCase):
    def test_snaps_floats_to_integer_cells(self):
        self.assertEqual(cell_of((1.0000001, 0.9999, 2.4)), (1, 1, 2))

    def test_handles_negative_coordinates(self):
        self.assertEqual(cell_of((-0.6, -1.2, -3.0)), (-1, -1, -3))


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_add_and_get(self):
        self.board.add((0, 0, 0), 'block')
        self.assertEqual(self.board.get((0, 0, 0)), 'block')
        self.assertIn((0, 0, 0), self.board)
        self.assertEqual(len(self.board), 1)

    def test_cannot_add_twice_to_same_cell(self):
        self.board.add((0, 0, 0), 'block')
        with self.assertRaises(ValueError):
            self.board.add((0, 0, 0), 'other')

    def test_remove_returns_block_and_frees_cell(self):
        self.board.add((1, 0, 1), 'block')
        self.assertEqual(self.board.remove((1, 0, 1)), 'block')
        self.assertNotIn((1, 0, 1), self.board)

    def test_remove_empty_cell_is_safe(self):
        self.assertIsNone(self.board.remove((5, 5, 5)))

    def test_cannot_place_on_occupied_cell(self):
        self.board.add((0, 0, 0), 'block')
        self.assertFalse(self.board.can_place((0, 0, 0)))

    def test_can_place_on_empty_cell_far_from_player(self):
        self.assertTrue(self.board.can_place((10, 0, 10), feet=(0, 0, 0)))

    def test_cannot_place_inside_player(self):
        # Player standing at feet (3, 1, 3): the cell they occupy is blocked.
        self.assertFalse(self.board.can_place((3, 1, 3), feet=(3, 1, 3)))


class VisibilityTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        # A solid 3x3x3 cube of blocks
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.board.add((x, y, z), 'dirt')

    def test_centre_block_is_hidden(self):
        self.assertFalse(self.board.is_visible((1, 1, 1)))

    def test_surface_block_is_visible(self):
        self.assertTrue(self.board.is_visible((1, 2, 1)))

    def test_removing_a_block_exposes_its_neighbour(self):
        self.assertFalse(self.board.is_visible((1, 1, 1)))
        self.board.remove((1, 2, 1))
        self.assertTrue(self.board.is_visible((1, 1, 1)))


class NeighbourTests(unittest.TestCase):
    def test_six_face_neighbours(self):
        self.assertEqual(len(neighbours((0, 0, 0))), 6)
        self.assertIn((0, 1, 0), neighbours((0, 0, 0)))


class OverlapsPlayerTests(unittest.TestCase):
    def test_block_at_feet_level_overlaps(self):
        self.assertTrue(overlaps_player((0, 0, 0), (0, 0, 0)))

    def test_block_beside_player_does_not_overlap(self):
        self.assertFalse(overlaps_player((3, 0, 0), (0, 0, 0)))

    def test_block_far_below_player_does_not_overlap(self):
        self.assertFalse(overlaps_player((0, -5, 0), (0, 0, 0)))


if __name__ == '__main__':
    unittest.main()
