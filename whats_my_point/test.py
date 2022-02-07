#!/usr/bin/env python3.10

# this is not part of any production system
# I did not bother to write proper testing
import unittest
from itertools import zip_longest
from numpy import array, ndarray

from whats_my_point import (
    Point,
    Vector,
    IntPoint,
    create_RoundedNPoint_class,
    iter_linearly_between,
)
from whats_my_point import IntPoint


class TestVector(unittest.TestCase):
    def test_basic_creation(self):
        v1 = Vector(1, 2, 3)
        self.assertTrue(v1 == (1, 2, 3))
        v3 = Vector((4, 5, 6))
        self.assertTrue(v3 == (4, 5, 6))
        v4 = Vector([4, 5, 6])
        self.assertTrue(v4 == (4, 5, 6))
        v5 = Vector(i + 4 for i in range(3))
        self.assertTrue(v5 == (4, 5, 6))

        # vector accepts weird input
        v6 = Vector((11, 26), 4)
        self.assertTrue(v6 == ((11, 26), 4))

    def test_identity(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(v1)
        self.assertTrue(v1 is v2)

    def test_create_from_numpy(self):
        v5 = Vector(i + 4 for i in range(3))
        an_ndarray = array(v5)
        v6 = Vector(an_ndarray)
        self.assertTrue(isinstance(v6, Vector))
        self.assertTrue(v6 == (4, 5, 6))
        another_ndarray = array(v6)
        self.assertTrue(tuple(another_ndarray), v6)


class TestPoint(unittest.TestCase):
    def test_creation(self):
        p1 = Point(1, 3)
        self.assertTrue(isinstance(p1, Point))
        self.assertTrue(p1.x == 1)
        self.assertTrue(p1.y == 3)
        self.assertTrue(p1 == (1, 3))

        p2 = Point(5, 6, 7)
        self.assertTrue(isinstance(p2, Point))
        self.assertTrue(p2.x == 5)
        self.assertTrue(p2.y == 6)
        self.assertTrue(p2.z == 7)
        self.assertTrue(p2 == (5, 6, 7))

        t1 = (9, 17)
        p4 = Point(t1)
        self.assertTrue(isinstance(p4, Point))
        self.assertTrue(p4.x == 9)
        self.assertTrue(p4.y == 17)
        self.assertTrue(p4 == (9, 17))

        t2 = (9, 17, 46)
        p5 = Point(t2)
        self.assertTrue(isinstance(p5, Point))
        self.assertTrue(p5.x == 9)
        self.assertTrue(p5.y == 17)
        self.assertTrue(p5.z == 46)
        self.assertTrue(p5 == (9, 17, 46))

    def test_identity(self):
        p1 = Point(1, 3)
        p3 = Point(p1)
        self.assertTrue(isinstance(p3, Point))
        self.assertTrue(p3 is p1)

    def test_bad_input(self):
        try:
            Point((11, 26), 4)
        except TypeError as e:
            self.assertTrue("(11, 26)" in str(e))
        try:
            Point("x", "y", "z")
        except TypeError as e:
            self.assertTrue("x" in str(e))

    def test_addition(self):
        p1 = Point(1, 3)
        p4 = Point(9, 17)
        p8 = p1 + p4
        self.assertTrue(isinstance(p8, Point))
        self.assertTrue(p8.x == 10)
        self.assertTrue(p8.y == 20)
        self.assertTrue(p8 == (10, 20))

        p9 = p8 + 1
        self.assertTrue(p9.x == 11)
        self.assertTrue(p9.y == 21)
        self.assertTrue(p9 == (11, 21))

    def test_multiplication(self):
        p1 = Point(1, 3)
        p9 = p1 * 2
        self.assertTrue(p9.x == 2)
        self.assertTrue(p9.y == 6)
        self.assertTrue(p9 == (2, 6))

        p8 = Point(2.0, 4.0) * Point(2, 2)
        self.assertTrue(isinstance(p8, Point))
        self.assertTrue(p8.x == 4.0)
        self.assertTrue(p8.y == 8.0)
        self.assertTrue(p8 == (4.0, 8.0))

        p9 = p1 * 2.0
        self.assertTrue(p9.x == 2.0)
        self.assertTrue(p9.y == 6.0)
        self.assertTrue(p9 == (2.0, 6.0))

    def test_math_with_numpy(self):
        nd1 = array(range(4))
        p10 = Point(nd1)
        p11 = p10 + nd1
        self.assertTrue(isinstance(p11, Point))
        self.assertTrue(p11 == (0, 2, 4, 6))
        nd2 = nd1 + p10
        self.assertTrue(isinstance(nd2, ndarray))
        self.assertTrue(p11 == Point(nd2))

    def test_transform(self):
        # identity transform
        p1 = Point(1, 3)
        trans1 = array(((1, 0), (0, 1)))
        p11 = p1.transform(trans1)
        self.assertTrue(p1 == p11)

        # scaling
        trans2 = array(((2, 0), (0, 3)))
        p12 = p1.transform(trans2)
        self.assertTrue(p12 == p1 * (2, 3))

        # rotation
        trans3 = array(((0, -1), (1, 0)))
        p13 = p1.transform(trans3)
        self.assertTrue(p13 == (-3, 1))


class TestRoundedPoint(unittest.TestCase):
    def test_IntPoint(self):
        self.assertEqual(IntPoint.__name__, "IntPoint")

        ip = IntPoint(1, 2, 3)
        self.assertEqual(ip, (1, 2, 3))

        ip = IntPoint(1.1, 2.5, 3.8)
        self.assertEqual(ip, (1, 2, 4))

        p = Point(9.9, 10, -2.2)
        ip = IntPoint(p)
        self.assertEqual(ip, (10, 10, -2))

    def test_Rounded2Point(self):
        Rounded2Point = create_RoundedNPoint_class(2)
        self.assertEqual(Rounded2Point.__name__, "Rounded2Point")

        ip = Rounded2Point(1.1111, 2.222, 3.3333)
        self.assertEqual(ip, (1.11, 2.22, 3.33))

        ip = Rounded2Point(1.111, 2.225, 3.336)
        # The y component of the result looks odd because of
        # the inability of float data type to correctly do
        # base 10 Bankers' Rounding for many cases
        self.assertEqual(ip, (1.11, 2.23, 3.34))

    def test_Rounded8Point(self):
        Rounded2Point = create_RoundedNPoint_class(8)
        self.assertEqual(Rounded2Point.__name__, "Rounded8Point")

        ip = Rounded2Point(1.1111111111, 2.22222222222, 3.3333333333)
        self.assertEqual(ip, (1.11111111, 2.22222222, 3.33333333))

        ip = Rounded2Point(1.11111111, 2.222222225, 3.3333333333)
        # note the difference in the result for the y in test_Rounded2Point
        # above. For floats, sometimes a 5 rounds up, sometimes it rounds down.
        self.assertEqual(ip, (1.11111111, 2.22222222, 3.33333333))


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
