#!/usr/bin/env python3.10

# this is not part of any production system
# I did not bother to write proper testing
import unittest

from whats_my_point import (
    Point,
    Vector,
    IntPoint,
    create_significant_digits_Point_class,
)
from whats_my_point.polar import PolarPoint
from numpy import array, ndarray
from math import pi


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
            self.assertTrue('(11, 26)' in str(e))
        try:
            Point("x", "y", "z")
        except TypeError as e:
            self.assertTrue('x' in str(e))

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


if __name__ == '__main__':
    unittest.main()
