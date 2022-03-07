#!/usr/bin/env python3.10

import unittest
from itertools import cycle
from collections.abc import Iterable
from math import pi as π
from whats_my_point import Vector, CartesianPoint, PolarPoint, iter_linearly_between

from whats_my_point.path import Path


class TestPath(unittest.TestCase):
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

    def assertEqual(self, first, second):
        # extend assertAlmostEqual to work with types based on Iterable
        match first, second:
            case [Iterable(), Iterable()]:
                for first_element, second_element in zip(first, second):
                    super().assertEqual(first_element, second_element)
            case _:
                super().assertEqual(first, second)

    def test_assert_almost_equal(self):
        self.assertAlmostEqual(3.00000000001, 3.0)
        self.assertRaises(AssertionError, self.assertAlmostEqual, 3, 4)
        self.assertRaises(
            AssertionError,
            self.assertAlmostEqual,
            ((2, 2, 2), (2, 3, 4)),
            ((2, 2, 2), (2, 4, 3)),
        )

    def test_create_with_iterator(self):
        cp1 = CartesianPoint(0, 0)
        cp2 = CartesianPoint(100, 150)
        path1 = Path(iter_linearly_between(cp1, cp2, 5))
        self.assertAlmostEqual(
            path1, ((0.0, 0.0), (20.0, 30.0), (40.0, 60.0), (60.0, 90.0), (80.0, 120.0))
        )

    def test_create_identity(self):
        cp1 = CartesianPoint(0, 0)
        cp2 = CartesianPoint(100, 150)
        path1 = Path(iter_linearly_between(cp1, cp2, 5))
        path2 = Path(path1)
        self.assertTrue(path2 is path1)

    def test_create_with_args(self):
        v1 = Vector(PolarPoint(1, π), PolarPoint(2, π / 2), PolarPoint(4, 0))
        path3 = Path(v1)
        self.assertAlmostEqual(path3, ((1, π), (2, π / 2), (4, 0)))

    def test_addition_with_scalar(self):
        cp1 = CartesianPoint(0, 0)
        cp2 = CartesianPoint(100, 150)
        path1 = Path(iter_linearly_between(cp1, cp2, 5))
        path2 = path1 + 1
        self.assertAlmostEqual(
            path2, ((1.0, 1.0), (21.0, 31.0), (41.0, 61.0), (61.0, 91.0), (81.0, 121.0))
        )
        self.assertEqual((x.__class__ for x in path2), cycle((CartesianPoint,)))

    def test_addition_with_point(self):
        cp1 = CartesianPoint(0, 0)
        cp2 = CartesianPoint(100, 150)
        path1 = Path(iter_linearly_between(cp1, cp2, 5))
        path2 = path1 + CartesianPoint(1, 2)
        self.assertAlmostEqual(
            path2, ((1.0, 2.0), (21.0, 32.0), (41.0, 62.0), (61.0, 92.0), (81.0, 122.0))
        )
        self.assertEqual((x.__class__ for x in path2), cycle((CartesianPoint,)))

    def test_addition_with_polarpoint(self):
        cp1 = CartesianPoint(0, 0)
        cp2 = CartesianPoint(100, 150)
        path1 = Path(iter_linearly_between(cp1, cp2, 5))
        path2 = path1 + PolarPoint(10, π / 2)
        self.assertAlmostEqual(
            path2,
            (
                (0.0, 10.0),
                (20.0, 40.0),
                (40.0, 70.0),
                (60.0, 100.0),
                (80.0, 130.0),
            ),
        )
        self.assertEqual((x.__class__ for x in path2), cycle((CartesianPoint,)))

    def test_polar_addition_with_polarpoint(self):
        cp1 = PolarPoint(0, 0)
        cp2 = PolarPoint(100, 2.0 * π)
        path1 = Path(iter_linearly_between(cp1, cp2, 4, PolarPoint))
        path2 = path1 + PolarPoint(10, π / 2)
        self.assertAlmostEqual(
            path2,
            (
                PolarPoint(0, 0) + PolarPoint(10, π / 2),
                PolarPoint(25, π / 2.0) + PolarPoint(10, π / 2),
                PolarPoint(50, π) + PolarPoint(10, π / 2),
                PolarPoint(75, 6.0 * π / 4.0) + PolarPoint(10, π / 2),
            ),
        )
        self.assertEqual((x.__class__ for x in path2), cycle((PolarPoint,)))

    def test_multiplication_with_scalar(self):
        cp1 = CartesianPoint(0, 0)
        cp2 = CartesianPoint(100, 150)
        path1 = Path(iter_linearly_between(cp1, cp2, 5))
        path2 = path1 * 2
        self.assertAlmostEqual(
            path2,
            ((0.0, 0.0), (40.0, 60.0), (80.0, 120.0), (120.0, 180.0), (160.0, 240.0)),
        )
        self.assertEqual((x.__class__ for x in path2), cycle((CartesianPoint,)))

    def test_multiplication_with_cartesian(self):
        cp1 = CartesianPoint(0, 0)
        cp2 = CartesianPoint(100, 150)
        path1 = Path(iter_linearly_between(cp1, cp2, 5))
        path2 = path1 * CartesianPoint(2, 3)
        self.assertAlmostEqual(
            path2,
            ((0.0, 0.0), (40.0, 90.0), (80.0, 180.0), (120.0, 270.0), (160.0, 360.0)),
        )
        self.assertEqual((x.__class__ for x in path2), cycle((CartesianPoint,)))


if __name__ == "__main__":
    unittest.main()
