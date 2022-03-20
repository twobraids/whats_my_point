from collections.abc import Iterable
from numbers import Number
from math import sin, cos, sqrt, atan2

from points import Vector, CartesianPoint


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

    @classmethod
    def as_polar(cls, a_cartesian_point, target_polar_class=None):
        # The base point type in this system is cartesian. Any classes within the family that
        # iterpret coordinates differently must provide conversion both to and from cartesian.
        if target_polar_class is None:
            target_polar_class = cls
        match a_cartesian_point:
            case (x, y, z):
                # 3D case
                return target_polar_class(
                    sqrt((x**2) + (y**2) + (z**2)),
                    atan2(y, x),
                    atan2(sqrt((x**2) + (y**2)), z),
                )

            case (x, y):
                # 2D case
                return target_polar_class(
                    sqrt((x**2) + (y**2)),
                    atan2(y, x),
                )

            case _:
                raise TypeError(
                    f"Points must be 2D or 3D. Don't know how to convert {a_cartesian_point} to Polar"
                )

    def as_cartesian(self, cartesian_point_class=CartesianPoint):
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

    @classmethod
    def as_my_type(cls, the_other):
        # This function is in charge of converting things into polar coordinates.
        # The base class Vector has no sense of what its members mean, so members of the
        # polar branch of the Vector family interpret base Vector instances and other
        # Iterables as having polar values already.
        match the_other:
            case cls():
                # identity case
                return the_other

            case CartesianPoint() as a_cartesian_point:
                # we know this is the cartesian case, so we must explicitly convert it
                return cls.as_polar(a_cartesian_point)

            case Iterable() as an_iterator:
                # we don't know what this sequence represents.
                # To be consistent with the constructor, assume they are
                # series of components of a polar point
                return cls(*an_iterator)

            case Number() as ρ:
                # a rare case where a PolarPoint is specified with ρ alone and
                # θ, φ are assumed to be zero.
                return cls(ρ)

            case _:
                raise TypeError(f"Don't know how to convert {the_other} to Polar")

    # Arithmetic with polar coordinates directly is possible, but it's rather nightmarishly complex.
    # Since cartesian points are the base type, all arithmetic with PolarPoints is done by
    # converting to cartesian first and then converting back to polar afterwards.
    # In each case, the parameter, 'the_other', gets converted to cartesian only if necessary.
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
