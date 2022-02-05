#!/usr/bin/env python3.10

import unittest
from math import pi as π
from whats_my_point.polar import PolarPoint
from whats_my_point import Point, IntPoint
from collections.abc import Iterable

round


class TestConversions(unittest.TestCase):
    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        # extend assertAlmostEqual to work with types based on Iterable
        match first, second:
            case[Iterable(), Iterable()]:
                for first_element, second_element in zip(first, second):
                    super().assertAlmostEqual(first_element, second_element, places, msg, delta)
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

    def test_more_conversions(self):
        cp = Point(70.71, 70.71)
        ip = IntPoint(cp)
        self.assertEqual(ip, (71, 71))
        pp = PolarPoint(cp)
        cp2 = Point(pp)
        self.assertAlmostEqual(cp, cp2, 8)


if __name__ == "__main__":
    unittest.main()
