#!/usr/bin/env python3.10

import unittest
from collections.abc import Iterable
from math import pi as π

from whats_my_point import Vector, Point, IntPoint, PolarPoint


class TestConversions(unittest.TestCase):
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

    def test_Vector_from_known_types(self):
        v = Vector(π, π)
        cp = Point(2, 0)
        cp_args = (2, 16)
        ip = IntPoint(3, 4)
        pp = PolarPoint(10, π)

        v_v = Vector(v)
        self.assertTrue(v_v is v)

        v_cp = Vector(cp)
        self.assertTrue(v_cp is cp)

        v_ip = Vector(ip)
        self.assertTrue(v_ip is ip)

        v_pp = Vector(pp)
        self.assertTrue(v_pp is pp)

        v_a = Vector(cp_args)
        self.assertTrue(v_a is not cp_args)
        self.assertTrue(v_a.__class__ is Vector)
        self.assertEqual(v_a, cp_args)

    def test_Point_from_known_types(self):
        v = Vector(π, π)
        cp = Point(2, 0)
        cp_args = (2, 16)
        ip = IntPoint(3, 4)
        pp = PolarPoint(10, π)

        cp_v = Point(v)
        self.assertTrue(cp_v is not v)
        self.assertEqual(cp_v, v)
        self.assertTrue(cp_v.__class__ is Point)

        cp_cp = Point(cp)
        self.assertTrue(cp_cp is cp)

        cp_ip = Point(ip)
        self.assertTrue(cp_ip is ip)

        cp_pp = Point(pp)
        self.assertTrue(cp_pp is not pp)
        self.assertAlmostEqual(cp_pp, (-10.0, 0))
        self.assertTrue(cp_pp.__class__ is Point)

        cp_a = Point(cp_args)
        self.assertTrue(cp_a is not cp_args)
        self.assertEqual(cp_a, (2, 16))
        self.assertEqual(cp_a, cp_args)

    def test_IntPoint_from_known_types(self):
        v = Vector(π, π)
        cp = Point(2.1, 8.6)
        cp_args = (2, 16)
        ip = IntPoint(3, 4)
        pp = PolarPoint(10, π / 4)

        ip_v = IntPoint(v)
        self.assertTrue(ip_v is not v)
        self.assertEqual(ip_v, (3, 3))
        self.assertTrue(ip_v.__class__ is IntPoint)

        ip_cp = IntPoint(cp)
        self.assertTrue(ip_cp is not cp)
        self.assertEqual(ip_cp, (2, 9))
        self.assertTrue(ip_cp.__class__ is IntPoint)

        ip_ip = IntPoint(ip)
        self.assertTrue(ip_ip is ip)

        ip_pp = IntPoint(pp)
        self.assertTrue(ip_pp is not pp)
        self.assertEqual(ip_pp, (7, 7))
        self.assertTrue(ip_pp.__class__ is IntPoint)

        ip_a = IntPoint(cp_args)
        self.assertTrue(ip_a is not cp_args)
        self.assertEqual(ip_a, cp_args)
        self.assertTrue(ip_a.__class__ is IntPoint)

    def test_PolarPoint_from_known_types(self):
        v = Vector(π, π / 4)
        cp = Point(2.1, 8.6)
        ip = IntPoint(3, 4)
        pp = PolarPoint(10, π)
        pp_args = (10, π / 4.0)

        # vector have no meta data here if they are Cartesian or Polar
        # the constructor must trust that the values are appropriately Polar
        pp_v = PolarPoint(v)
        self.assertTrue(pp_v is not v)
        self.assertEqual(pp_v, (π, π / 4), 8)
        self.assertTrue(pp_v.__class__ is PolarPoint)

        pp_cp = PolarPoint(cp)
        self.assertTrue(pp_cp is not cp)
        self.assertAlmostEqual(pp_cp, (8.852683209061531, 1.3312970608847376), 8)
        self.assertTrue(pp_cp.__class__ is PolarPoint)

        pp_ip = PolarPoint(ip)
        self.assertTrue(pp_ip is not cp)
        self.assertAlmostEqual(pp_ip, (5, 0.9272952180016122), 8)
        self.assertTrue(pp_ip.__class__ is PolarPoint)

        pp_pp = PolarPoint(pp)
        self.assertTrue(pp_pp is pp)

        pp_a = PolarPoint(pp_args)
        self.assertTrue(pp_a is not pp_args)
        self.assertAlmostEqual(pp_a, (10, 0.7853981633974483), 8)
        self.assertTrue(pp_a.__class__ is PolarPoint)

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

    def test_more_conversions(self):
        cp = Point(70.71, 70.71)
        ip = IntPoint(cp)
        self.assertEqual(ip, (71, 71))
        pp = PolarPoint(cp)
        cp2 = Point(pp)
        self.assertAlmostEqual(cp, cp2, 8)

    def test_math_with_polar_and_cartesion(self):
        pp1 = PolarPoint(10, 0)
        cp1 = Point(10, 0)
        self.assertEqual(pp1 + cp1, (20, 0))
        self.assertEqual(cp1 + cp1, (20, 0))

        pp2 = PolarPoint(10, π)
        cp2 = Point(2, 0)
        cp3 = cp2 + pp2
        self.assertAlmostEqual(cp3, (-8.0, 0), 8)
        self.assertTrue(isinstance(cp3, Point))
        pp3 = pp2 + cp2
        self.assertAlmostEqual(pp3, (8.0, π), 8)
        self.assertTrue(isinstance(pp3, PolarPoint))

        pp4 = PolarPoint(10, π * 1.75)
        cp4 = Point(0, -10)
        self.assertEqual(pp4 + cp4, PolarPoint(cp4 + pp4))

    def test_failure_of_math_with_polar_and_cartesian(self):
        pp = PolarPoint(range(5))
        cp = Point((i * 10 for i in range(5)))
        self.assertRaises(TypeError, lambda a, b: a + b, pp, cp)
        self.assertRaises(TypeError, lambda a, b: b + a, pp, cp)

    def test_math_with_polar_and_scalar(self):
        pp1 = PolarPoint(10, π / 3.0)
        cp1 = Point(2, 2)
        self.assertEqual(pp1 + 2, pp1 + cp1)
        self.assertEqual(pp1 * 2, pp1 * cp1)
        self.assertEqual(pp1 / 2, pp1 / cp1)
        self.assertEqual(pp1 // 2, pp1 // cp1)
        self.assertEqual(pp1**2, pp1**cp1)

    def test_as_my_type_1(self):
        cp1 = Point(2.2, 3.3)
        ip1 = IntPoint(4, 5)
        ip2 = ip1.as_my_type(cp1)
        self.assertTrue(isinstance(ip2, IntPoint))
        self.assertEqual(ip2, (2, 3))

    def test_as_my_type_2(self):
        cp1 = Point(2.2, 3.3)
        ip1 = IntPoint(4, 5)
        cp2 = cp1.as_my_type(ip1)
        self.assertTrue(isinstance(cp2, Point))
        self.assertEqual(cp2, (4.0, 5.0))

    def test_as_my_type_3(self):
        cp1 = Point(10, 10)
        pp1 = PolarPoint(cp1)
        pp2 = pp1.as_my_type(cp1)
        self.assertEqual(pp1, pp2)

    def test_as_my_type_4(self):
        pp1 = PolarPoint(10, π / 3.0)
        pp2 = pp1.as_my_type(3)
        self.assertEqual(pp2, (3,))

    def test_as_my_type_5(self):
        cp1 = Point(range(5))
        pp1 = PolarPoint(10, π / 3.0)
        self.assertRaises(TypeError, pp1.as_my_type, cp1)


if __name__ == "__main__":
    unittest.main()
