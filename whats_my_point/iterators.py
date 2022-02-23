from whats_my_point import CartesianPoint


def no_consectutive_repeats_iter(an_iterator):
    previous_value = None
    for a_value in an_iterator:
        if a_value != previous_value:
            yield a_value
        previous_value = a_value


def linear_transform(start, stop, number_of_iterations):
    increment = (stop - start) / number_of_iterations
    for i in range(number_of_iterations):
        yield start + (increment * i)


def iter_linearly_between(
    start_point, end_point, number_of_iterations, target_point_type=CartesianPoint
):
    base_point_type = start_point.__class__
    for p in zip(
        *(
            linear_transform(x, y, number_of_iterations)
            for x, y in zip(start_point, end_point)
        )
    ):
        yield target_point_type(base_point_type(*p))
