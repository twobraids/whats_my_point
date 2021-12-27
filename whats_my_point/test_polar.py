#!/usr/bin/env python3.10

import unittest
from whats_my_point.polar import PolarPoint
from whats_my_point import (
    Point,
    IntPoint,
)
from math import pi


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


if __name__ == '__main__':
    unittest.main()
