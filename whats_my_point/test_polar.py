#!/usr/bin/env python3.10

import unittest
from math import pi as π
from itertools import zip_longest
from collections.abc import Iterable

from whats_my_point.polar import PolarPoint
from whats_my_point import Point, IntPoint, iter_linearly_between


class TestConversions(unittest.TestCase):
    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        # extend assertAlmostEqual to work with types based on Iterable
        match first, second:
            case [Iterable(), Iterable()]:
                for first_element, second_element in zip(first, second):
                    super().assertAlmostEqual(
                        first_element, second_element, places, msg, delta
                    )
            case _:
                super().assertAlmostEqual(first, second, places, msg, delta)

    def test_polar_to_cartesian_by_constructor(self):
        pp = PolarPoint(1, π / 2.0)
        cp = IntPoint(pp)
        self.assertEqual(cp, Point(0, 1))

        pp = PolarPoint(1, π)
        cp = IntPoint(pp)
        self.assertEqual(cp, Point(-1, 0))

    def test_cartesian_to_polar_by_constructor_2D_round_trip(self):
        pp1 = PolarPoint(1, π / 2.0)
        cp = Point(pp1)
        pp2 = PolarPoint(cp)
        self.assertEqual(pp1, pp2)

        pp1 = PolarPoint(1, π + π / 2.0)
        cp = Point(pp1)
        pp2 = PolarPoint(cp)
        self.assertEqual(pp2.r, pp1.r)
        # here θ is the same angle, but measured from the other direction
        # the sum of two such angles should be π
        self.assertAlmostEqual(pp2.θ + pp1.θ, π, 8)
        cp2 = Point(pp2)
        self.assertAlmostEqual(cp2, cp, 8)

    def test_cartesian_to_polar_by_constructor_3D_round_trip(self):
        pp3 = PolarPoint(1, π + π / 2.0, 3 * π / 5.0)
        cp1 = Point(pp3)
        pp4 = PolarPoint(cp1)
        self.assertEqual(pp4.r, pp3.r)
        # here θ is the same angle, but measured from the other direction
        # the sum of two such angles should be π
        self.assertAlmostEqual(pp4.θ + pp3.θ, π, 8)
        self.assertAlmostEqual(pp4.φ, pp3.φ, 8)

        cp2 = Point(pp4)
        self.assertAlmostEqual(cp2, cp1)

    def test_more_conversions(self):
        cp = Point(70.71, 70.71)
        ip = IntPoint(cp)
        self.assertEqual(ip, (71, 71))
        pp = PolarPoint(cp)
        cp2 = Point(pp)
        self.assertAlmostEqual(cp, cp2, 8)

    def test_adding_two_2D_polars(self):
        # along the x axis
        pp1 = PolarPoint(1, 0)
        pp2 = PolarPoint(2, 0)
        self.assertEqual(pp1 + pp2, PolarPoint(3, 0))

        # along the x axis
        pp1 = PolarPoint(1, 0)
        pp2 = PolarPoint(2, π)
        self.assertEqual(pp1 + pp2, PolarPoint(1, π))

        # with a perpenticular
        pp1 = PolarPoint(4, 0)
        pp2 = PolarPoint(4, π / 2.0)
        pp_sum = pp1 + pp2
        self.assertAlmostEqual(pp_sum, (5.656854249492381, π / 4.0), 8)

        cp = Point(pp_sum)
        self.assertAlmostEqual(cp, (4.0, 4.0), 8)

    def test_math_with_polar_and_cartesion(self):
        pp1 = PolarPoint(10, 0)
        cp1 = Point(10, 0)
        self.assertEqual(pp1 + cp1, (20, 0))
        self.assertEqual(cp1 + cp1, (20, 0))

        pp2 = PolarPoint(10, π)
        cp2 = Point(2, 0)
        cp3 = cp2 + pp2
        self.assertAlmostEqual(cp3, (-8.0, 0), 8)
        self.assertTrue(isinstance(cp3, Point))
        cp3 = pp2 + cp2
        self.assertAlmostEqual(pp2 + cp2, (8.0, π), 8)
        self.assertTrue(isinstance(cp3, PolarPoint))

        pp4 = PolarPoint(10, π * 1.75)
        cp4 = Point(0, -10)




    def test_math_with_polar_and_scalar(self):
        pp1 = PolarPoint(10, π / 3.0)
        cp1 = Point(2, 2)
        self.assertEqual(pp1 + 2, pp1 + cp1)
        self.assertEqual(pp1 * 2, pp1 * cp1)
        self.assertEqual(pp1 / 2, pp1 / cp1)
        self.assertEqual(pp1 // 2, pp1 // cp1)
        self.assertEqual(pp1**2, pp1**cp1)


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
        pp1 = PolarPoint(10, 0)
        pp2 = PolarPoint(10, π / 4)

        expected_result_sequence = (
            Point(10.0, 0.0),
            Point(9.807852804032304, 1.9509032201612824),
            Point(9.238795325112868, 3.826834323650898),
            Point(8.314696123025453, 5.555702330196022),
        )
        # this function automatically requests that the iter_linear_transition convert to
        # same type as the type of the first item in the expected_result_sequence
        self.compare_sequences(
            pp1, pp2, 4, iter_linearly_between, expected_result_sequence
        )

        expected_result_sequence = (
            PolarPoint(10.0, 0.0),
            PolarPoint(10.0, 0.19634954084936207),
            PolarPoint(10.0, 0.39269908169872414),
            PolarPoint(10.0, 0.5890486225480862),
        )
        self.compare_sequences(
            pp1, pp2, 4, iter_linearly_between, expected_result_sequence
        )


if __name__ == "__main__":
    unittest.main()
