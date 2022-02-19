from collections.abc import Iterable
from itertools import zip_longest, starmap
from numbers import Number
from operator import sub, add, mul, truediv, floordiv, pow


class Vector(tuple):
    def __new__(cls, *args):
        match (args):
            case [cls() as a_lone_cls_instance_from_args]:
                return a_lone_cls_instance_from_args

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
        match the_other:
            case cls():
                return the_other
            case _:
                return cls(the_other)

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

            case Vector() as a_vector:
                the_other_as_my_type = self.convert_to_my_type(a_vector)
                return self.__class__(
                    *starmap(a_dyadic_fn, zip(self, the_other_as_my_type))
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

    def __pow__(self, the_other):
        return self._operation(the_other, pow)

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
        # or something with a similar Aπ
        return self.__class__(a_transform_matrix.dot(self))
