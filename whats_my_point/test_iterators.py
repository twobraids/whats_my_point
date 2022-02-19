#!/usr/bin/env python3.10

import unittest
from itertools import zip_longest

from whats_my_point import Point, IntPoint, iter_linearly_between


class TestIters(unittest.TestCase):
    def compare_sequences(
        self,
        start_polar_point,
        end_polar_point,
        iterations,
        iter_fn,
        expected_point_sequence,
    ):
        expected_length = len(expected_point_sequence) - 1
        for i, (a_point, expected_point) in enumerate(
            zip_longest(
                iter_fn(
                    start_polar_point,
                    end_polar_point,
                    iterations,
                    expected_point_sequence[0].__class__,
                ),
                expected_point_sequence,
            )
        ):
            self.assertEqual(
                a_point,
                expected_point,
                f"[{i}] {a_point} is not the same as {expected_point} ",
            )
        self.assertFalse(
            i < expected_length,
            f"iterator produced too few: expected {expected_length} not {i}",
        )
        self.assertFalse(
            i > expected_length,
            f"iterator produced too many: expected {expected_length} not {i}",
        )

    def test_iter_all_linear(self):
        start_point = Point(10, 0)
        end_point = Point(0, 10)

        expected_result_sequence = (
            Point(10.0, 0.0),
            Point(8.0, 2.0),
            Point(6.0, 4.0),
            Point(4.0, 6.0),
            Point(2.0, 8.0),
        )
        self.compare_sequences(
            start_point, end_point, 5, iter_linearly_between, expected_result_sequence
        )

        expected_result_sequence = (
            IntPoint(10, 0),
            IntPoint(8, 2),
            IntPoint(6, 4),
            IntPoint(4, 6),
            IntPoint(2, 8),
        )
        # this function automatically requests that the iter_linear_transition convert to
        # same type as the type of the first item in the expected_result_sequence
        self.compare_sequences(
            start_point, end_point, 5, iter_linearly_between, expected_result_sequence
        )


if __name__ == "__main__":
    unittest.main()
