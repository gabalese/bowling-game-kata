from bowling.game.game import Game
import unittest


class BowlingGameTestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def roll_many(self, times, pins):
        for i in range(times):
            self.game.roll(pins)

    def test_gutter_game(self):
        self.roll_many(20, 0)
        self.assertEquals(0, self.game.score())

    def test_all_ones(self):
        self.roll_many(20, 1)
        self.assertEquals(20, self.game.score())

    def test_one_spare_and_nulls(self):
        self.game.roll(5)
        self.game.roll(5)
        self.roll_many(18, 0)
        self.assertEquals(10, self.game.score())

    def test_one_spare_and_ones(self):
        self.game.roll(5)
        self.game.roll(5)
        self.roll_many(18, 1)
        self.assertEquals(29, self.game.score())

    def test_one_spare_points_then_nulls(self):
        self.game.roll(6)
        self.game.roll(4)
        self.game.roll(3)
        self.roll_many(17, 0)
        self.assertEquals(16, self.game.score())

    def test_one_spare_points_then_points(self):
        self.game.roll(6)
        self.game.roll(4)
        self.game.roll(4)
        self.roll_many(17, 0)
        self.assertEquals(18, self.game.score())

    def test_one_strike_and_nulls(self):
        self.game.roll(10)
        self.roll_many(18, 0)
        self.assertEquals(10, self.game.score())

    def test_one_strike_and_ones(self):
        self.game.roll(10)
        self.game.roll(1)
        self.game.roll(1)
        self.roll_many(16, 0)
        self.assertEquals(14, self.game.score())

    def test_perfect_game(self):
        self.roll_many(9, 10)
        self.game.roll(10)
        self.game.roll(10)
        self.game.roll(10)
        self.assertEquals(300, self.game.score())


if __name__ == '__main__':
    unittest.main()
