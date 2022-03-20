#!/usr/bin/env python3.10
import unittest
from numpy import array, ndarray

from points import Vector


class TestVector(unittest.TestCase):
    def test_basic_creation(self):
        v1 = Vector(1, 2, 3)
        self.assertEqual(v1, (1, 2, 3))
        v3 = Vector((4, 5, 6))
        self.assertEqual(v3, (4, 5, 6))
        v4 = Vector([4, 5, 6])
        self.assertEqual(v4, (4, 5, 6))

    def test_identity(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(v1)
        self.assertTrue(v1 is v2)

    def test_create_from_numpy(self):
        v5 = Vector(i + 4 for i in range(3))
        an_ndarray = array(v5)
        v6 = Vector(an_ndarray)
        self.assertTrue(isinstance(v6, Vector))
        self.assertEqual(v6, (4, 5, 6))
        self.assertEqual(v6, tuple(an_ndarray))
        another_ndarray = array(v6)
        self.assertEqual(tuple(another_ndarray), v6)

    def test_create_with_iterator(self):
        v1 = Vector(range(3))
        self.assertEqual(v1, (0, 1, 2))
        v5 = Vector(i + 4 for i in range(3))
        self.assertEqual(v5, (4, 5, 6))

    def test_crazy_inputs(self):
        v7 = Vector("now", "is", "the", "time")
        self.assertEqual(len(v7), 4)
        v8 = Vector((1, 2), (3, 4), (6, 7))
        self.assertEqual(len(v8), 3)
        v9 = Vector("nope", (1, 2, 3), range(10))
        self.assertEqual(len(v9), 3)

    def test_addition(self):
        v1 = Vector(1, 3)
        v4 = Vector(9, 17)
        v8 = v1 + v4
        self.assertTrue(isinstance(v8, Vector))
        self.assertEqual(v8[0], 10)
        self.assertEqual(v8[1], 20)
        self.assertEqual(v8, (10, 20))

        v9 = v8 + 1
        self.assertEqual(v9[0], 11)
        self.assertEqual(v9[1], 21)
        self.assertEqual(v9, (11, 21))

    def test_multiplication(self):
        v1 = Vector(1, 3)
        v9 = v1 * 2
        self.assertEqual(v9[0], 2)
        self.assertEqual(v9[1], 6)
        self.assertEqual(v9, (2, 6))

        v8 = Vector(2.0, 4.0) * Vector(2, 2)
        self.assertTrue(isinstance(v8, Vector))
        self.assertEqual(v8[0], 4.0)
        self.assertEqual(v8[1], 8.0)
        self.assertEqual(v8, (4.0, 8.0))

        v9 = v1 * 2.0
        self.assertEqual(v9[0], 2.0)
        self.assertEqual(v9[1], 6.0)
        self.assertEqual(v9, (2.0, 6.0))

    def test_math_with_numpy(self):
        nd1 = array(range(4))
        v10 = Vector(nd1)
        v11 = v10 + nd1
        self.assertTrue(isinstance(v11, Vector))
        self.assertEqual(v11, (0, 2, 4, 6))
        nd2 = nd1 + v10
        self.assertTrue(isinstance(nd2, ndarray))
        self.assertEqual(v11, Vector(nd2))


if __name__ == "__main__":
    unittest.main()
