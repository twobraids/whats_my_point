from numbers import Number
from whats_my_point import Vector


def no_consectutive_repeats_iter(an_iterator):
    previous_value = None
    for a_value in an_iterator:
        if a_value != previous_value:
            yield a_value
        previous_value = a_value


def iter_uniform_steps_between(
    start, stop, number_of_iterations, target_type=lambda n: n
):
    match start:
        case Number():
            increment = (stop - start) / number_of_iterations
            for i in range(number_of_iterations):
                yield target_type(start + (increment * i))

        case Vector():
            base_point_type = start.__class__
            for p in zip(
                *(
                    iter_uniform_steps_between(x, y, number_of_iterations)
                    for x, y in zip(start, stop)
                )
            ):
                yield target_type(base_point_type(*p))

        case _:
            raise TypeError(
                f'start value must be scalar or Vector type: {start} is not.'
            )
