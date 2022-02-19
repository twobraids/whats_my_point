#!/usr/bin/env python3.10

import unittest
from math import pi as π
from itertools import zip_longest
from collections.abc import Iterable

from whats_my_point import Vector, Point, IntPoint, PolarPoint


class TestPolar(unittest.TestCase):
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

    def test_polar_constructor_1(self):
        pp = PolarPoint(1, π / 2.0)
        self.assertEqual(len(pp), 2)
        self.assertTrue(isinstance(pp, PolarPoint))
        self.assertAlmostEqual(pp, (1, 1.5707963267948966), 8)
        self.assertEqual(pp.rho, 1)
        self.assertEqual(pp.r, 1)
        self.assertEqual(pp.ρ, 1)
        self.assertAlmostEqual(pp.theta, 1.5707963267948966)
        self.assertAlmostEqual(pp.θ, 1.5707963267948966)
        self.assertAlmostEqual(pp.phi, 0)
        self.assertAlmostEqual(pp.φ, 0)

    def test_polar_constructor_2(self):
        pp = PolarPoint(1, π / 2.0, π)
        self.assertEqual(len(pp), 3)
        self.assertTrue(isinstance(pp, PolarPoint))
        self.assertAlmostEqual(pp, (1, 1.5707963267948966, π), 8)
        self.assertEqual(pp.rho, 1)
        self.assertEqual(pp.r, 1)
        self.assertEqual(pp.ρ, 1)
        self.assertAlmostEqual(pp.theta, 1.5707963267948966)
        self.assertAlmostEqual(pp.θ, 1.5707963267948966)
        self.assertAlmostEqual(pp.phi, π)
        self.assertAlmostEqual(pp.φ, π)

    def test_polar_constructor_3(self):
        # greater than 3D is fine for creation
        # but we can't do much with it
        pp = PolarPoint(range(5))
        self.assertEqual(pp, (0, 1, 2, 3, 4))
        self.assertRaises(TypeError, lambda a: a**2, pp)

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


if __name__ == "__main__":
    unittest.main()
