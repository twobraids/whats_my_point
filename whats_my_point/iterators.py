def no_consectutive_repeats_iter(an_iterator):
    previous_value = None
    for a_value in an_iterator:
        if a_value != previous_value:
            yield a_value
        previous_value = a_value


def iter_uniform_steps_between(
    start, stop, number_of_iterations, target_type=lambda n: n
):
    increment = (stop - start) / number_of_iterations
    for i in range(number_of_iterations):
        yield target_type(start + (increment * i))
