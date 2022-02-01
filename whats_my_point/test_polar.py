#!/usr/bin/env python3.10

import unittest
from math import pi
from whats_my_point.polar import PolarPoint
from whats_my_point import Point, IntPoint


class TestConversions(unittest.TestCase):
    def test_polar_to_cartesian_by_constructor(self):
        pp = PolarPoint(1, pi / 2.0)
        cp = IntPoint(pp)
        self.assertEqual(cp, Point(0, 1))

        pp = PolarPoint(1, pi)
        cp = IntPoint(pp)
        self.assertEqual(cp, Point(-1, 0))

    def test_cartesian_to_polar_by_constructor_2D_round_trip(self):
        pp1 = PolarPoint(1, pi / 2.0)
        cp = Point(pp1)
        pp2 = PolarPoint(cp)
        self.assertEqual(pp1, pp2)

        pp1 = PolarPoint(1, pi + pi / 2.0)
        cp = Point(pp1)
        pp2 = PolarPoint(cp)
        self.assertEqual(pp2.r, pp1.r)
        # here θ is the same angle, but from coming from a different direction
        # the sum of two such angles should be pi
        self.assertAlmostEqual(pp2.θ + pp1.θ, pi, 8)
        cp2 = Point(pp2)
        self.assertEqual(cp2, cp)

    def test_cartesian_to_polar_by_constructor_3D_round_trip(self):
        pp3 = PolarPoint(1, pi + pi / 2.0, 3 * pi / 5.0)
        cp1 = Point(pp3)
        pp4 = PolarPoint(cp1)
        self.assertEqual(pp4.r, pp3.r)
        # here θ is the same angle, but from coming from a different direction
        # the sum of two such angles should be pi
        self.assertAlmostEqual(pp4.θ + pp3.θ, pi, 8)
        self.assertAlmostEqual(pp4.φ, pp3.φ, 8)
        cp2 = Point(pp4)
        self.assertEqual(cp2, cp1)

    def test_adding_two_2D_polars(self):
        # along the x axis
        pp1 = PolarPoint(1, 0)
        pp2 = PolarPoint(2, 0)
        self.assertEqual(pp1 + pp2, PolarPoint(3, 0))

        # along the x axis
        pp1 = PolarPoint(1, 0)
        pp2 = PolarPoint(2, pi)
        self.assertEqual(pp1 + pp2, PolarPoint(1, pi))

        # with a perpenticular
        pp1 = PolarPoint(4, 0)
        pp2 = PolarPoint(4, pi / 2.0)
        pp_sum = pp1 + pp2
        self.assertAlmostEqual(pp_sum.r, 5.65685, 4)
        self.assertAlmostEqual(pp_sum.θ, pi / 4.0, 8)
        cp = Point(pp_sum)
        self.assertEqual(cp, Point(4.0, 4.0))


if __name__ == '__main__':
    unittest.main()
