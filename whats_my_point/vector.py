from collections.abc import Iterable
from itertools import zip_longest, starmap
from numbers import Number
from operator import sub, add, mul, truediv, floordiv, pow


class Vector(tuple):
    def __new__(cls, *args):
        match (args):
            case [cls() as an_instance_of_cls]:
                # match instances of the calling cls or its derivatives
                # this is the identity case
                return an_instance_of_cls

            case [Vector() as an_instance_of_vector]:
                # match any instance of the Vector family not directly in line with cls
                # explicitly invoke a conversion - maybe cartesian to polar or vice versa
                return cls.as_my_type(an_instance_of_vector)

            case [Iterable() as an_iterable]:
                # match any old iterable like a generator or numpy array
                # create a new instance of this cls
                return super().__new__(
                    cls,
                    tuple(cls._judge_candidate_value(n) for n in an_iterable),
                )

            case args_:
                # discrete values were passed, assume they are to be the coordinate
                # values of a new instance of this cls
                return super().__new__(
                    cls, tuple(cls._judge_candidate_value(n) for n in args_)
                )

    @staticmethod
    def _judge_candidate_value(a_candidate):
        # Subclasses can override this method to restrict potential component members
        # by considering characteristics like type or value. Unacceptable candidates
        # should raise a TypeError. Acceptable candidates should be returned.
        return a_candidate

    @classmethod
    def as_my_type(cls, the_other):
        # Subclasses ought to override this method to reflect conversions for different
        # interpretations of the vector components.
        match the_other:
            case cls():
                # match of this cls or its derivatives
                return the_other
            case _:
                # match anything else such as tuple or iterable.
                # try to construct a new cls instance directly from the_other
                return cls(the_other)

    def _operation(self, the_other, a_dyadic_fn):
        # return a new instance with members that result from a_dyadic_fn applied to
        # this instance zipped with the_other
        match (the_other):
            case Number() as a_number:
                # match scalars
                return self.__class__(
                    *starmap(
                        a_dyadic_fn, zip_longest(self, (a_number,), fillvalue=a_number)
                    )
                )

            case Vector() as a_vector:
                # match any instance of the Vector family
                the_other_as_my_type = self.as_my_type(a_vector)
                return self.__class__(
                    *starmap(a_dyadic_fn, zip(self, the_other_as_my_type))
                )

            case Iterable() as an_iterable:
                # match any other type of iterable
                return self.__class__(*starmap(a_dyadic_fn, zip(self, an_iterable)))

            case _:
                # no idea how to apply this value in a dyadic manner with this Vector instance
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
