# make these symbols importable from the package level
from whats_my_point.vector import Vector
from whats_my_point.cartesian import (
    CartesianPoint,
    IntPoint,
    create_RoundedNPoint_class,
)

Point = CartesianPoint

from whats_my_point.polar import PolarPoint
from whats_my_point.iterators import no_consectutive_repeats_iter, iter_linearly_between
