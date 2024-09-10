# Copyright (c) Maxwell Bernstein
import omegastar
import unittest


class BisectTests(unittest.TestCase):
    def test_succeeding_with_full_items_raises_value_error(self):
        def command(items):
            return True

        with self.assertRaisesRegex(ValueError, "with full items"):
            omegastar.run_bisect(command, [1, 2, 3])

    def test_failing_with_empty_items_raises_value_error(self):
        def command(items):
            return False

        with self.assertRaisesRegex(ValueError, "with empty items"):
            omegastar.run_bisect(command, [1, 2, 3])

    def test_bisect_one(self):
        def command(items):
            return 2 not in items

        self.assertEqual(omegastar.run_bisect(command, [1, 2, 3, 4, 5]), [2])

    def test_bisect_two(self):
        def command(items):
            return not (1 in items and 5 in items)

        self.assertEqual(omegastar.run_bisect(command, [1, 2, 3, 4, 5]), [1, 5])

    def test_bisect_three(self):
        def command(items):
            return not (1 in items and 3 in items and 5 in items)

        self.assertEqual(omegastar.run_bisect(command, [1, 2, 3, 4, 5]), [1, 3, 5])

    def test_bisect_n(self):
        n_steps = 0

        def command(items):
            nonlocal n_steps
            n_steps += 1
            return not (-5 in items and 1 in items and 3 in items and 5 in items)

        self.assertEqual(
            omegastar.run_bisect(command, list(range(-1_000_000, 1_000_000))),
            [-5, 1, 3, 5],
        )
        self.assertEqual(n_steps, 69)


if __name__ == "__main__":
    unittest.main()
