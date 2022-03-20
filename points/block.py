from collections.abc import Iterable
from enum import IntFlag
from numbers import Number
from itertools import chain


from points import Point, IntPoint, PolarPoint
from points.path import Path


class Position(IntFlag):
    INSIDE = 0
    BELOW_XMIN = 1
    ABOVE_XMAX = 2
    BELOW_YMIN = 4
    ABOVE_YMAX = 8
    BELOW_XMIN_BELOW_YMIN = BELOW_XMIN | BELOW_YMIN
    BELOW_XMIN_ABOVE_YMAX = BELOW_XMIN | ABOVE_YMAX
    ABOVE_XMAX_BELOW_YMIN = ABOVE_XMAX | BELOW_YMIN
    ABOVE_XMAX_ABOVE_YMAX = ABOVE_XMAX | ABOVE_YMAX


class Block(Path):
    # blocks always exist in the cartesian world
    @staticmethod
    def min_max_points(a, b, c, d, target_point_class=Point):
        min_x = min(a, c)
        max_x = max(a, c)
        min_y = min(b, d)
        max_y = max(b, d)
        return (target_point_class(min_x, min_y), target_point_class(max_x, max_y))

    def __new__(cls, *args):
        match args:
            case [cls() as a_block]:
                return a_block

            case [Path() as a_path]:
                path_length = len(a_path)
                if path_length == 2:
                    return cls.__new__(cls, *a_path)
                elif path_length == 1:
                    return cls.__new__(cls, Point(0, 0), *a_path)
                raise ValueError(
                    f"{cls} can only accept a {a_path.__class__} length of 1 or 2, {a_path} isn't right"
                )

            case [PolarPoint() as pp1]:
                return cls.__new__(cls, Point(0, 0), Point(pp1))

            case [PolarPoint() as pp1, PolarPoint() as pp2]:
                return cls.__new__(cls, Point(pp1), Point(pp2))

            case [Point()]:
                return super().__new__(
                    cls, *cls.min_max_points(0, 0, args[0].x, args[0].y)
                )

            case [Point() as p1, Point() as p2]:
                return super().__new__(cls, *cls.min_max_points(*p1, *p2))

            case [Number(), Number()]:
                return super().__new__(cls, *cls.min_max_points(0, 0, *args))

            case [Number(), Number(), Number(), Number()]:
                return super().__new__(cls, *cls.min_max_points(*args))

            case [str() as a_string]:
                return cls.__new__(
                    cls, *(int(x.strip()) for x in a_string.split(",") if x.strip())
                )

            case [Iterable() as an_iterable]:
                materialized = tuple(an_iterable)
                materialized_length = len(materialized)
                if materialized_length in (1, 2):
                    return cls.__new__(cls, *(Point(x) for x in an_iterable))
                elif materialized_length == 4:
                    return cls.__new__(cls, *materialized)
                raise TypeError(f"{materialized} cannot be interpretted as a block")

            case _:
                raise TypeError(f"{args} does not make a {cls}")

    @property
    def upper_left(self):
        return self[0]

    min_point = upper_left

    @property
    def lower_right(self):
        return self[1]

    max_point = lower_right

    @property
    def upper_right(self):
        return Point(self[1].x, self[0].y)

    @property
    def lower_left(self):
        return Point(self[0].x, self[1].y)

    @property
    def upper(self):
        return self[0].y

    y_min = upper

    @property
    def lower(self):
        return self[1].y

    y_max = lower

    @property
    def left(self):
        return self[0].x

    x_min = left

    @property
    def right(self):
        return self[1].x

    x_max = right

    @property
    def center(self):
        return (self.lower_right - self.upper_left) / 2 + self.upper_left

    @property
    def size(self):
        return self.lower_right - self.upper_left

    def surrounds(self, a_point):
        a_cartesian_point = a_point.as_cartesian()
        return (self.x_min <= a_cartesian_point.x < self.x_max) and (
            self.y_min <= a_cartesian_point.y < self.y_max
        )

    def relative_point_position(self, a_point):
        point_position = Position.INSIDE

        if a_point.x < self.x_min:
            point_position |= Position.BELOW_XMIN
        elif a_point.x > self.x_max:
            point_position |= Position.ABOVE_XMAX

        if a_point.y < self.y_min:
            point_position |= Position.BELOW_YMIN
        elif a_point.y > self.y_max:
            point_position |= Position.ABOVE_YMAX

        return point_position

    def as_str(self):
        return ", ".join(str(a_scalar) for a_scalar in chain.from_iterable(self))


def block_as_str(a_block):
    return a_block.as_str()


class ClipException(Exception):
    pass


def clip_path_to_viewport(viewport_block, line_segment):
    """Cohen-Sutherland clipping algorithm"""

    x_min, y_min = viewport_block.min_point
    x_max, y_max = viewport_block.max_point

    x1, y1 = line_segment[0]
    x2, y2 = line_segment[1]

    first_point_position = viewport_block.relative_point_position(line_segment[0])
    second_point_position = viewport_block.relative_point_position(line_segment[1])

    while (
        first_point_position | second_point_position
    ) != Position.INSIDE:  # loop until both candidate are inside the viewport

        if (first_point_position & second_point_position) != Position.INSIDE:
            # the points are
            raise ClipException(f"entirely outside viewport: {line_segment}")

        a_position = first_point_position or second_point_position
        match a_position:
            case Position.ABOVE_YMAX | Position.ABOVE_XMAX_ABOVE_YMAX | Position.BELOW_XMIN_ABOVE_YMAX:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            case Position.BELOW_YMIN | Position.BELOW_XMIN_BELOW_YMIN | Position.ABOVE_XMAX_BELOW_YMIN:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            case Position.ABOVE_XMAX:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            case Position.BELOW_XMIN:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min
            case _:
                raise RuntimeError(f"Invalid position state {a_position}")

        if a_position is first_point_position:
            candidate_first_point = IntPoint(x, y)
            first_point_position = viewport_block.relative_point_position(
                candidate_first_point
            )
            x1, y1 = candidate_first_point

        elif a_position is second_point_position:
            candidate_second_point = IntPoint(x, y)
            second_point_position = viewport_block.relative_point_position(
                candidate_second_point
            )
            x2, y2 = candidate_second_point

    return Path(IntPoint(x1, y1), IntPoint(x2, y2))
