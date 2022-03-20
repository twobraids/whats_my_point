#!/usr/bin/env python3.10

import unittest
from math import pi as π
from collections.abc import Iterable
from points import CartesianPoint, PolarPoint
from points.path import Path
from points.block import Block, Position, clip_path_to_viewport, ClipException


class TestBlock(unittest.TestCase):
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

    def test_create_identity(self):
        b1 = Block(1, 2, 3, 4)
        b2 = Block(b1)
        self.assertTrue(b2 is b1)

    def test_create_with_scalars(self):
        b1 = Block(0, 5, 10, 20)
        self.assertEqual(b1.upper_left, (0, 5))
        self.assertEqual(b1.lower_right, (10, 20))
        self.assertEqual(b1.upper_right, (10, 5))
        self.assertEqual(b1.lower_left, (0, 20))
        self.assertEqual(b1.upper, 5)
        self.assertEqual(b1.lower, 20)
        self.assertEqual(b1.left, 0)
        self.assertEqual(b1.right, 10)
        self.assertEqual(b1.center, (5.0, 12.5))
        self.assertTrue(b1.surrounds(CartesianPoint(0, 5)))
        self.assertFalse(b1.surrounds(CartesianPoint(10, 20)))
        self.assertFalse(b1.surrounds(CartesianPoint(10, 5)))
        self.assertFalse(b1.surrounds(CartesianPoint(0, 20)))
        self.assertTrue(b1.surrounds(CartesianPoint(5.0, 12.5)))
        self.assertFalse(b1.surrounds(CartesianPoint(500, 1000)))

    def test_create_with_scalars_weird_order(self):
        b1 = Block(1000, 4000, 60, 5000)
        self.assertEqual(b1.upper_left, (60, 4000))
        self.assertEqual(b1.lower_right, (1000, 5000))
        self.assertEqual(b1.upper_right, (1000, 4000))
        self.assertEqual(b1.lower_left, (60, 5000))
        self.assertEqual(b1.upper, 4000)
        self.assertEqual(b1.lower, 5000)
        self.assertEqual(b1.left, 60)
        self.assertEqual(b1.right, 1000)
        self.assertEqual(b1.center, (530, 4500))
        self.assertTrue(b1.surrounds(CartesianPoint(60, 4000)))
        self.assertTrue(b1.surrounds(CartesianPoint(999, 4999)))
        self.assertFalse(b1.surrounds(CartesianPoint(1000, 5000)))
        self.assertTrue(b1.surrounds(CartesianPoint(999, 4000)))
        self.assertTrue(b1.surrounds(CartesianPoint(60, 4999)))
        self.assertTrue(b1.surrounds(CartesianPoint(530, 4500)))
        self.assertFalse(b1.surrounds(CartesianPoint(500, 1000)))

    def test_create_with_2_scalars(self):
        b1 = Block(10, 20)
        self.assertEqual(b1.upper_left, (0, 0))
        self.assertEqual(b1.lower_right, (10, 20))
        self.assertEqual(b1.upper_right, (10, 0))
        self.assertEqual(b1.lower_left, (0, 20))
        self.assertEqual(b1.upper, 0)
        self.assertEqual(b1.lower, 20)
        self.assertEqual(b1.left, 0)
        self.assertEqual(b1.right, 10)
        self.assertEqual(b1.center, (5.0, 10.0))
        self.assertTrue(b1.surrounds(CartesianPoint(0, 0)))
        self.assertFalse(b1.surrounds(CartesianPoint(10, 20)))
        self.assertFalse(b1.surrounds(CartesianPoint(10, 0)))
        self.assertFalse(b1.surrounds(CartesianPoint(0, 20)))
        self.assertTrue(b1.surrounds(CartesianPoint(5.0, 10)))
        self.assertFalse(b1.surrounds(CartesianPoint(500, 1000)))

    def test_create_with_points(self):
        p1 = CartesianPoint(0, 5)
        p2 = CartesianPoint(10, 20)
        b1 = Block(p1, p2)
        self.assertEqual(b1.upper_left, (0, 5))
        self.assertEqual(b1.lower_right, (10, 20))
        self.assertEqual(b1.upper_right, (10, 5))
        self.assertEqual(b1.lower_left, (0, 20))
        self.assertEqual(b1.upper, 5)
        self.assertEqual(b1.lower, 20)
        self.assertEqual(b1.left, 0)
        self.assertEqual(b1.right, 10)
        self.assertEqual(b1.center, (5.0, 12.5))
        self.assertTrue(b1.surrounds(CartesianPoint(0, 5)))
        self.assertFalse(b1.surrounds(CartesianPoint(10, 20)))
        self.assertTrue(b1.surrounds(CartesianPoint(9, 19)))
        self.assertTrue(b1.surrounds(CartesianPoint(9, 5)))
        self.assertTrue(b1.surrounds(CartesianPoint(0, 19)))
        self.assertTrue(b1.surrounds(CartesianPoint(5.0, 12.5)))
        self.assertFalse(b1.surrounds(CartesianPoint(500, 1000)))

    def test_create_with_points_weird_order(self):
        p1 = CartesianPoint(1000, 4000)
        p2 = CartesianPoint(60, 5000)
        b1 = Block(p1, p2)
        self.assertEqual(b1.upper_left, (60, 4000))
        self.assertEqual(b1.lower_right, (1000, 5000))
        self.assertEqual(b1.upper_right, (1000, 4000))
        self.assertEqual(b1.lower_left, (60, 5000))
        self.assertEqual(b1.upper, 4000)
        self.assertEqual(b1.lower, 5000)
        self.assertEqual(b1.left, 60)
        self.assertEqual(b1.right, 1000)
        self.assertEqual(b1.center, (530, 4500))
        self.assertTrue(b1.surrounds(CartesianPoint(60, 4000)))
        self.assertTrue(b1.surrounds(CartesianPoint(999, 4999)))
        self.assertTrue(b1.surrounds(CartesianPoint(999, 4000)))
        self.assertTrue(b1.surrounds(CartesianPoint(60, 4999)))
        self.assertTrue(b1.surrounds(CartesianPoint(530, 4500)))
        self.assertFalse(b1.surrounds(CartesianPoint(500, 1000)))

    def test_create_with_1_point(self):
        p2 = CartesianPoint(10, 20)
        b1 = Block(p2)
        self.assertEqual(b1.upper_left, (0, 0))
        self.assertEqual(b1.lower_right, (10, 20))
        self.assertEqual(b1.upper_right, (10, 0))
        self.assertEqual(b1.lower_left, (0, 20))
        self.assertEqual(b1.upper, 0)
        self.assertEqual(b1.lower, 20)
        self.assertEqual(b1.left, 0)
        self.assertEqual(b1.right, 10)
        self.assertEqual(b1.center, (5.0, 10.0))
        self.assertTrue(b1.surrounds(CartesianPoint(0, 0)))
        self.assertFalse(b1.surrounds(CartesianPoint(10, 20)))
        self.assertTrue(b1.surrounds(CartesianPoint(9, 0)))
        self.assertFalse(b1.surrounds(CartesianPoint(10, 0)))
        self.assertFalse(b1.surrounds(CartesianPoint(0, 20)))
        self.assertTrue(b1.surrounds(CartesianPoint(5.0, 10)))
        self.assertFalse(b1.surrounds(CartesianPoint(500, 1000)))

    def test_create_from_path(self):
        p1 = CartesianPoint(0, 5)
        p2 = CartesianPoint(10, 20)
        path1 = Path(p1, p2)
        b1 = Block(path1)
        self.assertEqual(b1, ((0, 5), (10, 20)))
        b2 = Block(p1, p2)
        self.assertEqual(b1, b2)

    def test_create_from_short_path(self):
        p2 = CartesianPoint(10, 20)
        path1 = Path((p2,))
        b1 = Block(path1)
        self.assertEqual(b1, ((0, 0), (10, 20)))

    def test_create_fail_from_path(self):
        p1 = CartesianPoint(0, 5)
        p2 = CartesianPoint(10, 20)
        p3 = CartesianPoint(100, 200)
        self.assertRaises(ValueError, Block, Path(p1, p2, p3))

    def test_create_with_one_polarpoint(self):
        pp1 = PolarPoint(10, 0)
        b1 = Block(pp1)
        self.assertEqual(b1[1], (10, 0))

    def test_create_with_polarpoints(self):
        pp1 = PolarPoint(10, 0)
        pp2 = PolarPoint(10, π / 2.0)
        b2 = Block(pp1, pp2)
        self.assertAlmostEqual(b2.upper_left, (0, 0))
        self.assertAlmostEqual(b2.lower_right, (10, 10))

    def test_create_with_tuple_iterables(self):
        t1 = ((0, 0), (3, 3))
        b1 = Block(t1)
        self.assertEqual(b1.upper_left, (0, 0))
        self.assertTrue(isinstance(b1.upper_left, CartesianPoint))
        self.assertEqual(b1.lower_right, (3, 3))
        self.assertTrue(isinstance(b1.lower_right, CartesianPoint))

    def test_create_with_scalar_iterables(self):
        t1 = (0, 0, 3, 3)
        b1 = Block(t1)
        self.assertEqual(b1.upper_left, (0, 0))
        self.assertTrue(isinstance(b1.upper_left, CartesianPoint))
        self.assertEqual(b1.lower_right, (3, 3))
        self.assertTrue(isinstance(b1.lower_right, CartesianPoint))

    def test_create_from_string(self):
        s = "100, 0, 0, 100"
        b1 = Block(s)
        self.assertEqual(b1.upper_left, (0, 0))
        self.assertTrue(isinstance(b1.upper_left, CartesianPoint))
        self.assertEqual(b1.lower_right, (100, 100))
        self.assertTrue(isinstance(b1.lower_right, CartesianPoint))

    def test_block_to_str(self):
        b1 = Block(0, 100, 100, 0)
        self.assertEqual(b1.as_str(), "0, 0, 100, 100")

        b2 = Block(3840, 2160)
        self.assertEqual(b2.as_str(), "0, 0, 3840, 2160")

    def test_center(self):
        b1 = Block(0, 100, 100, 0)
        self.assertEqual(b1.center, (50, 50))
        b2 = Block(-100, -100, 100, 100)
        self.assertEqual(b2.center, (0, 0))

    def test_size(self):
        b1 = Block(0, 0, 100, 100)
        self.assertEqual(b1.size, (100, 100))
        b2 = Block(-100, -100, 100, 100)
        self.assertEqual(b2.size, (200, 200))

    def test_surrounds(self):
        b1 = Block(0, 0, 100, 100)
        self.assertFalse(b1.surrounds(CartesianPoint(100, 100)))
        self.assertTrue(b1.surrounds(CartesianPoint(99, 99)))
        self.assertTrue(b1.surrounds(CartesianPoint(0, 0)))
        self.assertTrue(b1.surrounds(CartesianPoint(50, 50)))
        self.assertFalse(b1.surrounds(CartesianPoint(-50, -50)))
        self.assertFalse(b1.surrounds(CartesianPoint(0, -50)))
        self.assertFalse(b1.surrounds(CartesianPoint(150, 150)))
        self.assertFalse(b1.surrounds(CartesianPoint(150, 0)))
        self.assertFalse(b1.surrounds(CartesianPoint(0, 150)))

    def test_relative_point_position(self):
        b1 = Block(0, 0, 100, 100)
        self.assertTrue(
            b1.relative_point_position(CartesianPoint(100, 100)) == Position.INSIDE
        )
        self.assertTrue(
            b1.relative_point_position(CartesianPoint(0, 0)) == Position.INSIDE
        )
        self.assertTrue(
            b1.relative_point_position(CartesianPoint(50, 50)) == Position.INSIDE
        )

        self.assertTrue(
            b1.relative_point_position(CartesianPoint(-50, -50))
            & (Position.BELOW_XMIN | Position.BELOW_YMIN)
        )
        self.assertFalse(
            b1.relative_point_position(CartesianPoint(-50, -50))
            & (Position.ABOVE_XMAX | Position.ABOVE_YMAX)
        )

        self.assertTrue(
            b1.relative_point_position(CartesianPoint(0, -50)) & Position.BELOW_YMIN
        )
        self.assertFalse(
            b1.relative_point_position(CartesianPoint(0, -50))
            & (Position.BELOW_XMIN | Position.ABOVE_XMAX | Position.ABOVE_YMAX)
        )

        self.assertTrue(
            b1.relative_point_position(CartesianPoint(101, 101))
            & (Position.ABOVE_XMAX | Position.ABOVE_YMAX)
        )
        self.assertFalse(
            b1.relative_point_position(CartesianPoint(101, 101))
            & (Position.BELOW_XMIN | Position.BELOW_YMIN)
        )

        self.assertTrue(
            b1.relative_point_position(CartesianPoint(150, 0)) & Position.ABOVE_XMAX
        )
        self.assertFalse(
            b1.relative_point_position(CartesianPoint(150, 0))
            & (Position.BELOW_XMIN | Position.BELOW_YMIN | Position.ABOVE_YMAX)
        )

        self.assertTrue(
            b1.relative_point_position(CartesianPoint(0, 150)) & Position.ABOVE_YMAX
        )
        self.assertFalse(
            b1.relative_point_position(CartesianPoint(0, 150))
            & (Position.BELOW_XMIN | Position.ABOVE_XMAX | Position.BELOW_YMIN)
        )


class TestClipping(unittest.TestCase):
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

    def testInsideClip(self):
        viewport = Block(0, 0, 100, 100)
        a_line_segment = Path(CartesianPoint(10, 10), CartesianPoint(90, 90))
        clipped_line_segment = clip_path_to_viewport(viewport, a_line_segment)
        self.assertAlmostEqual(clipped_line_segment, a_line_segment)

    def testDiagonalClip(self):
        viewport = Block(0, 0, 100, 100)
        a_line_segment = Path(CartesianPoint(-10, -10), CartesianPoint(110, 110))
        clipped_line_segment = clip_path_to_viewport(viewport, a_line_segment)
        expected_clipped_line_segment = Path(
            CartesianPoint(0, 0), CartesianPoint(100, 100)
        )
        self.assertAlmostEqual(clipped_line_segment, expected_clipped_line_segment)

    def testDiagonalClip2(self):
        viewport = Block(0, 0, 100, 100)
        a_line_segment = Path(CartesianPoint(-10, 110), CartesianPoint(110, -10))
        clipped_line_segment = clip_path_to_viewport(viewport, a_line_segment)
        expected_clipped_line_segment = Path(
            CartesianPoint(0, 100), CartesianPoint(100, 0)
        )
        self.assertAlmostEqual(clipped_line_segment, expected_clipped_line_segment)

    def testOutsideClip(self):
        viewport = Block(0, 0, 100, 100)
        a_line_segment = Path(CartesianPoint(200, 200), CartesianPoint(300, 300))
        self.assertRaises(
            ClipException, clip_path_to_viewport, viewport, a_line_segment
        )

        a_line_segment = Path(CartesianPoint(-300, 300), CartesianPoint(300, 300))
        self.assertRaises(
            ClipException, clip_path_to_viewport, viewport, a_line_segment
        )

    def testHorizontalClip(self):
        viewport = Block(0, 0, 100, 100)
        a_line_segment = Path(CartesianPoint(-10, 50), CartesianPoint(110, 50))
        clipped_line_segment = clip_path_to_viewport(viewport, a_line_segment)
        expected_clipped_line_segment = Path(
            CartesianPoint(0, 50), CartesianPoint(100, 50)
        )
        self.assertAlmostEqual(clipped_line_segment, expected_clipped_line_segment)

    def testVerticalClip(self):
        viewport = Block(0, 0, 100, 100)
        a_line_segment = Path(CartesianPoint(50, -10), CartesianPoint(50, 110))
        clipped_line_segment = clip_path_to_viewport(viewport, a_line_segment)
        expected_clipped_line_segment = Path(
            CartesianPoint(50, 0), CartesianPoint(50, 100)
        )
        self.assertAlmostEqual(clipped_line_segment, expected_clipped_line_segment)

    def testPartialClip(self):
        viewport = Block(0, 0, 100, 100)
        a_line_segment = Path(CartesianPoint(-10, 15), CartesianPoint(15, -10))
        clipped_line_segment = clip_path_to_viewport(viewport, a_line_segment)
        expected_clipped_line_segment = Path(CartesianPoint(0, 5), CartesianPoint(5, 0))
        self.assertAlmostEqual(clipped_line_segment, expected_clipped_line_segment)


if __name__ == "__main__":
    unittest.main()
