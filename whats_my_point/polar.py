from numbers import Number
from math import sin, cos, sqrt, atan, pi, atan2


from . import Vector, Point


class PolarPoint(Vector):
    @classmethod
    def _judge_candidate_value(cls, a_potential_scalar):
        # accept only scalars as values
        if isinstance(a_potential_scalar, Number):
            return a_potential_scalar
        raise TypeError(f'{cls} members must be scalar, "{a_potential_scalar}" is not')

    @property
    def r(self):
        try:
            return self[0]
        except IndexError:
            return 0

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
            case [PolarPoint(), n]:
                return the_other

            case [Point() as p, 2]:
                return PolarPoint(
                    round(sqrt((p.x ** 2) + (p.y ** 2)), 10),
                    atan2(p.y, p.x),
                )

            case [Point() as p, 3]:
                return PolarPoint(
                   round(sqrt((p.x ** 2) + (p.y ** 2) + (p.z ** 2))),
                   atan2(p.y, p.x),
                   atan2(sqrt((p.x ** 2) + (p.y ** 2)), p.z)
                )

            case _:
                raise TypeError(f'No conversion defined for {the_other.__class__} to Polar Coordinates')

    def as_cartesian(self, cartesian_point_class=Point):
        match len(self):
            case 2:
                return cartesian_point_class(
                    round(self.r * cos(self.θ), 10),
                    round(self.r * sin(self.θ), 10),
                )

            case 3:
                return cartesian_point_class(
                    round(self.r * sin(self.φ) * cos(self.θ), 10),
                    round(self.r * sin(self.φ) * sin(self.θ), 10),
                    round(self.r * cos(self.φ), 10),
                )

            case _:
                raise TypeError(f'No conversion defined for coordinates with {len(self)} members')

    def as_polar(self, as_this_class):
        if as_this_class is self.__class__:
            return self
        else:
            return as_this_class(self)

        return None

    # arithmatic with polar coordinates is possible, but it is rather nightmarish
    # Cartesian points are the base type, so arithmatic done by convsion to Point types

    def __add__(self, the_other):
        return PolarPoint(self.as_cartesian().__add__(the_other.as_cartesian()))

    def __sub__(self, the_other):
        return self._operation(the_other, sub)

    def __mul__(self, the_other):
        return self._operation(the_other, mul)

    def __floordiv__(self, the_other):
        return self._operation(the_other, floordiv)

    def __truediv__(self, the_other):
        return self._operation(the_other, truediv)

    def __neg__(self):
        return self.__class__(*(-c for c in self))

    def trunc(self):
        return self.__class__(*(int(c) for c in self))

    def round(self):
        return self.__class__(*(round(c) for c in self))

    def dot(self, the_other):
        return sum(a * b for a, b in zip(self, the_other))
