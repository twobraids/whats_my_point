from collections.abc import Iterable
from itertools import zip_longest, starmap
from numbers import Number

from whats_my_point import Vector, CartesianPoint, PolarPoint


class Path(Vector):
    @classmethod
    def _judge_candidate_value(cls, a_potential_point):
        # accept only instances of Vector as values for a Path
        if isinstance(a_potential_point, Vector):
            return a_potential_point
        raise TypeError(
            f'{cls} members must be a Vector instance, "{a_potential_point}" is not'
        )

    def _operation(self, the_other, a_dyadic_fn):
        # return a new instance with members that result from a_dyadic_fn applied to
        # this instance zipped with the_other
        match the_other:
            case Number() as a_number:
                # match scalars
                return self.__class__(
                    *starmap(
                        a_dyadic_fn, zip_longest(self, (a_number,), fillvalue=a_number)
                    )
                )

            case self.__class__() as a_path_object:
                # match an instance of another Path
                return self.__class__(*starmap(a_dyadic_fn, zip(self, a_path_object)))

            case CartesianPoint() | PolarPoint():
                # match any instance of the two point families
                return self.__class__(
                    *starmap(
                        a_dyadic_fn,
                        zip_longest(self, (the_other,), fillvalue=the_other),
                    )
                )

            case Iterable() as an_iterable:
                # match any other type of iterable
                return self.__class__(*starmap(a_dyadic_fn, zip(self, an_iterable)))

            case _:
                # no idea how to apply this value in a dyadic manner with this Vector instance
                raise TypeError(f"{the_other} disallowed")
