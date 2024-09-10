import omegastar
import unittest


class BisectTests(unittest.TestCase):
    def test_succeeding_with_full_jitlist_raises_value_error(self):
        def command(jitlist):
            return True

        with self.assertRaisesRegex(ValueError, "with full jit-list"):
            omegastar.run_bisect(command, [1, 2, 3])

    def test_failing_with_empty_jitlist_raises_value_error(self):
        def command(jitlist):
            return False

        with self.assertRaisesRegex(ValueError, "with empty jit-list"):
            omegastar.run_bisect(command, [1, 2, 3])

    def test_bisect_one(self):
        def command(jitlist):
            return 2 not in jitlist

        self.assertEqual(omegastar.run_bisect(command, [1, 2, 3, 4, 5]), [2])

    def test_bisect_two(self):
        def command(jitlist):
            return not (1 in jitlist and 5 in jitlist)

        self.assertEqual(omegastar.run_bisect(command, [1, 2, 3, 4, 5]), [1, 5])

    def test_bisect_three(self):
        def command(jitlist):
            return not (1 in jitlist and 3 in jitlist and 5 in jitlist)

        self.assertEqual(omegastar.run_bisect(command, [1, 2, 3, 4, 5]), [1, 3, 5])


if __name__ == "__main__":
    unittest.main()
