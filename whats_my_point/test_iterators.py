#!/usr/bin/env python3.10

import unittest
from collections.abc import Iterable
from itertools import zip_longest
from math import pi as π

from whats_my_point import (
    CartesianPoint,
    IntPoint,
    PolarPoint,
    iter_linear_steps_between,
    Path,
)


class TestIters(unittest.TestCase):
    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        # extend assertAlmostEqual to work with types based on Iterable
        match first, second:
            case [Iterable(), Iterable()]:
                for i, (first_element, second_element) in enumerate(zip(first, second)):
                    try:
                        self.assertAlmostEqual(
                            first_element, second_element, places, msg, delta
                        )
                    except Exception as x:
                        raise AssertionError(
                            f"item #{i}, {first_element}, {second_element}: {str(x)}"
                        )
            case _:
                super().assertAlmostEqual(first, second, places, msg, delta)

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
            self.assertEqual(a_point.__class__, expected_point.__class__)
        self.assertFalse(
            i < expected_length,
            f"iterator produced too few: expected {expected_length} not {i}",
        )
        self.assertFalse(
            i > expected_length,
            f"iterator produced too many: expected {expected_length} not {i}",
        )

    def test_iter_cartesian_linear(self):
        start_point = CartesianPoint(10, 0)
        end_point = CartesianPoint(0, 10)

        expected_result_sequence = (
            CartesianPoint(10.0, 0.0),
            CartesianPoint(8.0, 2.0),
            CartesianPoint(6.0, 4.0),
            CartesianPoint(4.0, 6.0),
            CartesianPoint(2.0, 8.0),
        )
        self.compare_sequences(
            start_point,
            end_point,
            5,
            iter_linear_steps_between,
            expected_result_sequence,
        )

    def test_iter_intpoint_linear(self):
        start_point = IntPoint(10, 0)
        end_point = IntPoint(0, 10)

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
            start_point,
            end_point,
            5,
            iter_linear_steps_between,
            expected_result_sequence,
        )

    def test_iter_polarpoint_linear(self):
        cp1 = CartesianPoint(10, 0)
        cp2 = CartesianPoint(20, π / 2.0)
        expected_result_CartesianPoint_sequence = Path(
            CartesianPoint(10, 0),
            CartesianPoint(12.0, 0.3141592653589793),
            CartesianPoint(14.0, 0.6283185307179586),
            CartesianPoint(16.0, 0.9424777960769379),
            CartesianPoint(18.0, 1.2566370614359172),
        )
        cpath1 = Path(p for p in iter_linear_steps_between(cp1, cp2, 5))
        for p1, e1 in zip(cpath1, expected_result_CartesianPoint_sequence):
            self.assertEqual(p1, e1)

        polar_start_point = PolarPoint(cp1)
        polar_end_point = PolarPoint(cp2)
        expected_result_PolarPoint_sequence = Path(
            PolarPoint(p) for p in expected_result_CartesianPoint_sequence
        )
        eee = Path(CartesianPoint(p) for p in expected_result_PolarPoint_sequence)
        for p1, e1 in zip(eee, expected_result_CartesianPoint_sequence):
            self.assertAlmostEqual(p1, e1)

        ppath1 = Path(
            p for p in iter_linear_steps_between(polar_start_point, polar_end_point, 5)
        )
        for p1, e1 in zip(ppath1, expected_result_PolarPoint_sequence):
            self.assertAlmostEqual(p1, e1)


if __name__ == "__main__":
    unittest.main()
