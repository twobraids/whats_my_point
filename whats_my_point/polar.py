from numbers import Number
from math import sin, cos, sqrt, atan2


from . import Vector, Point


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

    ρ = rho
    r = rho

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

    # Point is the native coordinate type.  Any other type is responsible for coversions
    # both to and from that type.

    @classmethod
    def convert_to_my_type(cls, the_other):
        match the_other, len(the_other):
            case[PolarPoint(), _]:
                return the_other

            case[Point() as p, 2]:
                return cls(
                    sqrt((p.x**2) + (p.y**2)),
                    atan2(p.y, p.x),
                )

            case[Point() as p, 3]:
                return cls(
                    sqrt((p.x**2) + (p.y**2) + (p.z**2)),
                    atan2(p.y, p.x),
                    atan2(sqrt((p.x**2) + (p.y**2)), p.z),
                )

            case _:
                raise TypeError(
                    f"No conversion defined for {the_other.__class__} to Polar Coordinates"
                )

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
        return PolarPoint(self.as_cartesian() + the_other.as_cartesian())

    def __sub__(self, the_other):
        return PolarPoint(self.as_cartesian() - the_other.as_cartesian())

    def __mul__(self, the_other):
        return PolarPoint(self.as_cartesian() * the_other.as_cartesian())

    def __floordiv__(self, the_other):
        return PolarPoint(self.as_cartesian() // the_other.as_cartesian())

    def __truediv__(self, the_other):
        return PolarPoint(self.as_cartesian() / the_other.as_cartesian())

    def __neg__(self):
        return PolarPoint(-self.as_cartesian())

    def trunc(self):
        return PolarPoint(self.as_cartesian().trunc())

    def round(self):
        return PolarPoint(self.as_cartesian().round())

    def dot(self, the_other):
        return PolarPoint(self.as_cartesian().dot(the_other))
