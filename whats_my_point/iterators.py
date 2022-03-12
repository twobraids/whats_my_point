def no_consectutive_repeats_iter(an_iterator):
    previous_value = None
    for a_value in an_iterator:
        if a_value != previous_value:
            yield a_value
        previous_value = a_value


def iter_linear_steps_between(
    start, stop, number_of_iterations, target_type=lambda n: n
):
    # in cartesian space, make a sequence of points representing
    # a straight line between the start and stop points
    increment = (stop - start) / number_of_iterations
    for i in range(number_of_iterations):
        yield target_type(start + (increment * i))


def iter_natural_steps_between(
    start, stop, number_of_iterations, target_type=lambda n: n
):
    # In cartesian space, Vectors and CartesianPoints trace out straight
    # lines between the start and end points. PolarPoints trace curves
    # based on the full magnitude of the angular components (number of time
    # around the circle). I use this iterator for making spiral paths.
    base_point_type = start.__class__
    for p in zip(
        *(
            iter_linear_steps_between(first, second, number_of_iterations)
            for first, second in zip(start, stop)
        )
    ):
        yield target_type(base_point_type(*p))
