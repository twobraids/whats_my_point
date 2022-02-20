from collections.abc import Iterable
from numbers import Number
from math import sin, cos, sqrt, atan2

from math import pi as π


from whats_my_point import Vector, Point


class PolarPoint(Vector):
    @classmethod
    def _judge_candidate_value(cls, a_potential_scalar):
        # accept only scalars as values
        if isinstance(a_potential_scalar, Number):
            return a_potential_scalar
        raise TypeError(f'{cls} members must be scalar, "{a_potential_scalar}" is not')

    @property
    def rho(self):
        try:
            return self[0]
        except IndexError:
            return 0

    r = rho
    ρ = rho

    @property
    def theta(self):
        try:
            return self[1]
        except IndexError:
            return 0

    θ = theta

    @property
    def phi(self):
        try:
            return self[2]
        except IndexError:
            return 0

    φ = phi

    @staticmethod
    def len(n):
        try:
            return len(n)
        except TypeError:
            return None

    @classmethod
    def as_my_type(cls, the_other):
        # Point is the native coordinate type.  Any other type is responsible for coversions
        # both to and from that type.
        match the_other, cls.len(the_other):

            case [PolarPoint(), _]:
                # identity case
                return the_other

            case [Point() as p, 2]:
                # 2D Cartesion conversion case
                return cls(
                    sqrt((p.x**2) + (p.y**2)),
                    atan2(p.y, p.x),
                )

            case [Point() as p, 3]:
                # 3D Cartesion conversion case
                return cls(
                    sqrt((p.x**2) + (p.y**2) + (p.z**2)),
                    atan2(p.y, p.x),
                    atan2(sqrt((p.x**2) + (p.y**2)), p.z),
                )

            case [Point() as p, _]:
                # greater than 3D conversion case
                raise TypeError(
                    f"{the_other} is greater than 3D, don't know how to convert to Polar"
                )

            case [Iterable() as an_iterator, _]:
                # we don't know what this sequence represents.
                # To be consistent with the constructor, assume they are
                # series of components of a polar point
                return cls(*an_iterator)

            case [Number() as n, _]:
                # a rare case where ρ is n and θ, φ are zero.
                return cls(n)

            case _:
                raise TypeError(f"Don't know how to convert {the_other} to Polar")

    def as_cartesian(self, cartesian_point_class=Point):
        match len(self):
            case 2:
                return cartesian_point_class(
                    self.ρ * cos(self.θ),
                    self.ρ * sin(self.θ),
                )

            case 3:
                return cartesian_point_class(
                    self.ρ * sin(self.φ) * cos(self.θ),
                    self.ρ * sin(self.φ) * sin(self.θ),
                    self.ρ * cos(self.φ),
                )

            case _:
                raise TypeError(
                    f"No conversion defined for coordinates with {len(self)} members"
                )

    def as_polar(self, as_this_class):
        if as_this_class is self.__class__:
            return self
        else:
            return as_this_class(self)

        return None

    # arithmatic with polar coordinates is possible, but it is rather nightmarish
    # Cartesian points are the base type, so arithmatic done by convsion to Point types

    def __add__(self, the_other):
        return PolarPoint(self.as_cartesian() + the_other)

    def __sub__(self, the_other):
        return PolarPoint(self.as_cartesian() - the_other)

    def __mul__(self, the_other):
        return PolarPoint(self.as_cartesian() * the_other)

    def __floordiv__(self, the_other):
        return PolarPoint(self.as_cartesian() // the_other)

    def __truediv__(self, the_other):
        return PolarPoint(self.as_cartesian() / the_other)

    def __pow__(self, the_other):
        return PolarPoint(self.as_cartesian() ** the_other)

    def __neg__(self):
        return PolarPoint(-self.as_cartesian())

    def trunc(self):
        return PolarPoint(self.as_cartesian().trunc())

    def round(self):
        return PolarPoint(self.as_cartesian().round())

    def dot(self, the_other):
        return PolarPoint(self.as_cartesian().dot(the_other))
