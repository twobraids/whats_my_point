from itertools import zip_longest, starmap
from operator import sub, add, mul, truediv, floordiv
from numbers import Number
from collections.abc import Iterable


class Vector(tuple):
    def __new__(cls, *args):
        match (args):
            case [Vector() as a_lone_vector_from_args]:
                return cls.convert_to_my_type(a_lone_vector_from_args)

            case [Iterable() as a_lone_iterable_from_args]:
                return super().__new__(
                    cls,
                    tuple(
                        cls._judge_candidate_value(n) for n in a_lone_iterable_from_args
                    ),
                )

            case args_:
                return super().__new__(
                    cls, tuple(cls._judge_candidate_value(n) for n in args_)
                )

    @staticmethod
    def _judge_candidate_value(a_candidate):
        # Subclasses can override this method to restrict potential vector members
        # by considering characteristics like type or value. Unacceptable candidates
        # should raise a TypeError. Acceptable candidates should be returned.
        return a_candidate

    @classmethod
    def convert_to_my_type(cls, the_other):
        return the_other

    def _operation(self, the_other, a_dyadic_fn):
        # return a new instance with members that result from a_dyadic_fn applied to
        # this instance zipped with the_other
        match (the_other):
            case Number() as a_number:
                return self.__class__(
                    *starmap(
                        a_dyadic_fn, zip_longest(self, (a_number,), fillvalue=a_number)
                    )
                )

            case Iterable() as an_iterable:
                return self.__class__(*starmap(a_dyadic_fn, zip(self, an_iterable)))

            case _:
                raise TypeError(f"{the_other} disallowed")

    def __add__(self, the_other):
        return self._operation(the_other, add)

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

    def transform(self, a_transform_matrix):
        # a_transform_matrix intented to be a numpy ndarray
        # or something with a similar API
        return self.__class__(a_transform_matrix.dot(self))


class Point(Vector):
    @staticmethod
    def _judge_candidate_value(a_potential_scalar):
        # accept only scalars as values
        if isinstance(a_potential_scalar, Number):
            return a_potential_scalar
        raise TypeError(f"members must be scalar, {a_potential_scalar} is not")

    @classmethod
    def convert_to_my_type(cls, the_other):
        return the_other.as_cartesian(cls)

    def as_cartesian(self, as_this_class):
        if as_this_class is self.__class__:
            return self
        else:
            return as_this_class(self)

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


def create_significant_digits_Point_class(number_of_digits):
    class RoundedPoint(Point):
        def _judge_candidate_value(a_potential_scalar):
            # round all values up to a certain number of digits
            return round(a_potential_scalar, number_of_digits)

    return RoundedPoint


class IntPoint(Point):
    @staticmethod
    def _judge_candidate_value(a_potential_scalar):
        # round all values to an Integer
        return round(a_potential_scalar)
