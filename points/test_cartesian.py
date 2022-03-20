#!/usr/bin/env python3.10

import unittest
from numpy import array, ndarray

from points import (
    CartesianPoint,
    IntPoint,
    create_RoundedNPoint_class,
)


class TestPoint(unittest.TestCase):
    def test_creation(self):
        p1 = CartesianPoint(1, 3)
        self.assertTrue(isinstance(p1, CartesianPoint))
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 3)
        self.assertEqual(p1, (1, 3))

        p2 = CartesianPoint(5, 6, 7)
        self.assertTrue(isinstance(p2, CartesianPoint))
        self.assertEqual(p2.x, 5)
        self.assertEqual(p2.y, 6)
        self.assertEqual(p2.z, 7)
        self.assertEqual(p2, (5, 6, 7))

        t1 = (9, 17)
        p4 = CartesianPoint(t1)
        self.assertTrue(isinstance(p4, CartesianPoint))
        self.assertEqual(p4.x, 9)
        self.assertEqual(p4.y, 17)
        self.assertEqual(p4, (9, 17))

        t2 = (9, 17, 46)
        p5 = CartesianPoint(t2)
        self.assertTrue(isinstance(p5, CartesianPoint))
        self.assertEqual(p5.x, 9)
        self.assertEqual(p5.y, 17)
        self.assertEqual(p5.z, 46)
        self.assertEqual(p5, (9, 17, 46))

    def test_identity(self):
        p1 = CartesianPoint(1, 3)
        p3 = CartesianPoint(p1)
        self.assertTrue(isinstance(p3, CartesianPoint))
        self.assertTrue(p3 is p1)

    def test_bad_input(self):
        try:
            CartesianPoint((11, 26), 4)
        except TypeError as e:
            self.assertTrue("(11, 26)" in str(e))
        try:
            CartesianPoint("x", "y", "z")
        except TypeError as e:
            self.assertTrue("x" in str(e))

    def test_addition(self):
        p1 = CartesianPoint(1, 3)
        p4 = CartesianPoint(9, 17)
        p8 = p1 + p4
        self.assertTrue(isinstance(p8, CartesianPoint))
        self.assertEqual(p8.x, 10)
        self.assertEqual(p8.y, 20)
        self.assertEqual(p8, (10, 20))

        p9 = p8 + 1
        self.assertEqual(p9.x, 11)
        self.assertEqual(p9.y, 21)
        self.assertEqual(p9, (11, 21))

    def test_multiplication(self):
        p1 = CartesianPoint(1, 3)
        p9 = p1 * 2
        self.assertEqual(p9.x, 2)
        self.assertEqual(p9.y, 6)
        self.assertEqual(p9, (2, 6))

        p8 = CartesianPoint(2.0, 4.0) * CartesianPoint(2, 2)
        self.assertTrue(isinstance(p8, CartesianPoint))
        self.assertEqual(p8.x, 4.0)
        self.assertEqual(p8.y, 8.0)
        self.assertEqual(p8, (4.0, 8.0))

        p9 = p1 * 2.0
        self.assertEqual(p9.x, 2.0)
        self.assertEqual(p9.y, 6.0)
        self.assertEqual(p9, (2.0, 6.0))

    def test_math_with_numpy(self):
        nd1 = array(range(4))
        p10 = CartesianPoint(nd1)
        p11 = p10 + nd1
        self.assertTrue(isinstance(p11, CartesianPoint))
        self.assertEqual(p11, (0, 2, 4, 6))
        nd2 = nd1 + p10
        self.assertTrue(isinstance(nd2, ndarray))
        self.assertEqual(p11, CartesianPoint(nd2))


class TestRoundedPoint(unittest.TestCase):
    def test_IntPoint(self):
        self.assertEqual(IntPoint.__name__, "IntPoint")

        ip = IntPoint(1, 2, 3)
        self.assertEqual(ip, (1, 2, 3))

        ip = IntPoint(1.1, 2.5, 3.8)
        self.assertEqual(ip, (1, 2, 4))

        p = CartesianPoint(9.9, 10, -2.2)
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


if __name__ == "__main__":
    unittest.main()
