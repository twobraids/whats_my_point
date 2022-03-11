#!/usr/bin/env python3.10
from math import pi as π
from PIL import Image, ImageDraw

from whats_my_point import (
    CartesianPoint,
    PolarPoint,
    iter_uniform_steps_between,
    no_consectutive_repeats_iter,
)


class Canvas:
    # wrap the drawable image with a quicky interface to make the demo code look simpler.
    def __init__(self):
        self.the_image = Image.new("RGB", (900, 900), (0, 0, 0))
        self.the_drawable_image = ImageDraw.Draw(self.the_image)
        self.image_counter = 0
        self.previous_point = None

    def draw_successive_line_segment(self, end_point, step_counter):
        if self.previous_point is not None:
            self.the_drawable_image.line(
                (self.previous_point, end_point), fill="rgb(0, 255, 0)", width=4
            )
            if not (step_counter % 5):
                self.the_image.save(f"./spiral_{self.image_counter:04d}.png")
                self.image_counter += 1
        self.previous_point = end_point


def draw_a_looping_spiral(a_canvas):
    # the middle of the image
    cartesian_middle_point = CartesianPoint(a_canvas.the_image.size) / 2

    # beginning and end polar points for two loops around a circle
    # while the radius of the loop shrink
    larger_rotator_polar_origin = PolarPoint(cartesian_middle_point * (3.0 / 4.0, 0))
    larger_rotator_polar_destination = PolarPoint(0, 4.0 * π)
    larger_rotator_iter = iter_uniform_steps_between(
        larger_rotator_polar_origin, larger_rotator_polar_destination, 2000
    )

    # beginning and end polar points for fifty loops around a circle
    # with the loop radius shrinking with each step
    smaller_rotator_polar_origin = PolarPoint(cartesian_middle_point * (1.0 / 8.0, 0))
    smaller_rotator_polar_destination = PolarPoint(0, 100.0 * π)
    smaller_rotator_iter = iter_uniform_steps_between(
        smaller_rotator_polar_origin, smaller_rotator_polar_destination, 2000
    )

    # create a couple iterators that will produce a sequence of polar points
    # that spin in lockstep with each other
    for step_counter, (
        larger_rotated_polar_point,
        smaller_rotated_polar_point,
    ) in enumerate(
        no_consectutive_repeats_iter(
            zip(
                larger_rotator_iter,
                smaller_rotator_iter,
            )
        )
    ):
        # add the cartesian middle point with the spinning polar points
        current_cartesion_point = (
            cartesian_middle_point
            + larger_rotated_polar_point
            + smaller_rotated_polar_point
        )
        # draw the line segment from prevous and current cartesian points
        a_canvas.draw_successive_line_segment(current_cartesion_point, step_counter)


a_canvas = Canvas()
draw_a_looping_spiral(a_canvas)
