#!/usr/bin/env python3.10

AU_KM = 149597870.700


class unit(object):
    def __init__(self, name, conversion_factor=None, core_unit=None):
        self.name = name
        self.conversion_factor = conversion_factor
        self.core_unit = core_unit

    def __get__(self, instance, objtype=None):
        if instance is None:  # If called as a class method:

            def constructor(value):  # (same as above)
                obj = objtype.__new__(objtype)
                setattr(obj, self.name, value)
                conversion_factor = self.conversion_factor
                if conversion_factor is not None:
                    value = value / conversion_factor
                    setattr(obj, self.core_unit, value)
                return obj

            return constructor
        value = getattr(instance, self.core_unit)
        value = value * self.conversion_factor
        instance.__dict__[self.name] = value
        return value


class Distance:
    au = unit("au")
    km = unit("km", AU_KM, "au")


d = Distance.au(1.524)
print("au:", d.au)
print("km:", d.km)
print()
d = Distance.km(217)
print("au:", d.au)
print("km:", d.km)
