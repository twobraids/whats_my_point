#!/usr/bin/python3.10


class Point(tuple):

    def __new__(cls, *args):
        match(args):
            case (Point((0,0)) as a_point,):
                print(f"{a_point} is the point origin")
                return a_point
            case (Point() as a_point,):
                # args is tuple containing one Point
                return a_point
            case (tuple() as a_tuple,):
                # args is tuple containing one tuple
                return super().__new__(cls, a_tuple)
            case [(0,z) | (0,0,z)] as origin_tuple:
                print(f"{origin_tuple} is the tuple origin")
                return super().__new__(cls, args)
            case _:
                # args is a series of values
                return super().__new__(cls, args)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def __add__(self, the_other):
        if isinstance(the_other, int):
            return Point(*(int(i) + the_other for i in self))
        return Point(*(int(reduce(add, t)) for t in zip(self, the_other)))

    def __sub__(self, the_other):
        if isinstance(the_other, int):
            return Point(*(int(i - the_other) for i in self))
        return Point(*(int(reduce(sub, t)) for t in zip(self, the_other)))

    def __mul__(self, the_other):
        if isinstance(the_other, int):
            return Point(*(int(i * the_other) for i in self))
        return Point(*(reduce(mul, t) for t in zip(self, the_other)))

    def __floordiv__(self, the_other):
        if isinstance(the_other, int):
            return Point(*(i // the_other for i in self))
        return Point(*(reduce(floordiv, t) for t in zip(self, the_other)))

    def __truediv__(self, the_other):
        if isinstance(the_other, int):
            return Point(*(int(i / the_other) for i in self))
        return Point(*(reduce(truediv, t) for t in zip(self, the_other)))

    def __neg__(self):
        return Point(*(-c for c in self))

    def trunc(self):
        return Point(*(int(c) for c in self))

    def round(self):
        return Point(*(round(c) for c in self))


print(f'making p1')
p1 = Point(1, 3)
print(f'    p1 == {p1}')

print(f'making p2')
p2 = Point(5, 6)
print(f'    p2 == {p2}')

print(f'making p3')
p3 = Point(p1)
print(f'    p3 == {p3}')
print(f'    p3 is p1: {p3 is p1}')

print(f'making p4')
p4 = Point((9,17))
print(f'p4 == {p4}')

print(f'making p5')
p5 = Point((11, 26), 4)
print(f'p5 == {p5}')


print(f'making p6')
p6 = Point(0,0)
print(f'making p7')
p7 = Point(p6)

