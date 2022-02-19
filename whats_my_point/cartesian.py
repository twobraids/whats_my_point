from collections.abc import Iterable
from numbers import Number


from whats_my_point import Vector


class CartesianPoint(Vector):
    @staticmethod
    def _judge_candidate_value(a_potential_scalar):
        # accept only scalars as values
        if isinstance(a_potential_scalar, Number):
            return a_potential_scalar
        raise TypeError(f"members must be scalar, {a_potential_scalar} is not")

    @classmethod
    def as_my_type(cls, the_other):
        match (the_other):
            case cls():
                # Match an instance of this cls or its derivatives - identity case
                #   For example cls may be CartesianPoint but IntPoints would match
                #   an IntPoint is a CartesianPoint
                return the_other

            case Vector():
                # match an instance of base class Vector, but of another lineage than CartesianPoint
                try:
                    return the_other.as_cartesian(cls)
                except AttributeError:
                    # Vector itself doesn't know anything about cartesian, so just
                    # make a new instance of cls from it
                    return cls(*the_other)

            case Iterable():
                # make an instance of cls from any iterable
                return cls(*the_other)

            case _:
                raise TypeError(
                    f"No conversion defined for {the_other.__class__} to {cls}"
                )

    def as_cartesian(self, cartesian_point_class=None):
        if cartesian_point_class is None:
            return self
        return cartesian_point_class(*self)

    @property
    def x(self):
        try:
            return self[0]
        except IndexError:
            return 0

    @property
    def y(self):
        try:
            return self[1]
        except IndexError:
            return 0

    @property
    def z(self):
        try:
            return self[2]
        except IndexError:
            return 0


def create_RoundedNPoint_class(number_of_digits=None):
    class RoundedNPoint(CartesianPoint):
        def _judge_candidate_value(a_potential_scalar):
            # round all values up to a certain number of digits
            return round(a_potential_scalar, number_of_digits)

    if number_of_digits is None:
        RoundedNPoint.__name__ = "IntPoint"
    else:
        RoundedNPoint.__name__ = f"Rounded{number_of_digits}Point"
    return RoundedNPoint


Point = CartesianPoint
IntPoint = create_RoundedNPoint_class()
