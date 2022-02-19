#!/usr/bin/env python3.10
from math import pi as π
from PIL import Image, ImageDraw

from whats_my_point import (
    Point,
    PolarPoint,
    iter_linearly_between,
    iter_no_consectutive_repeats,
)

from whats_my_point.polar import PolarPoint


class Canvas:
    def __init__(self):
        self.an_image = Image.new("RGB", (400, 400), (0, 0, 0))
        self.a_drawable_image = ImageDraw.Draw(self.an_image)
        self.image_counter = 0
        self.previous_point = None

    def draw_successive_line_segment(self, end_point, step_counter):
        if self.previous_point is not None:
            self.a_drawable_image.line(
                (self.previous_point, end_point), fill="rgb(0, 255, 0)"
            )
            if not (step_counter % 5):
                self.an_image.save(f"./spiral_{self.image_counter:04d}.png")
                self.image_counter += 1
        self.previous_point = end_point


def looping_spiral(a_canvas):
    # the middle of a 600x600 image
    origin_point = Point(200, 200)
    # beginning and end polar points for two loops around a circle
    outer_rotator_origin = PolarPoint(150, 0)
    outer_rotator_destination = PolarPoint(0, 4.0 * π)
    # beginning and end polar points for fifty loops around a circle
    # with the loop diameter shrinking with each step
    inner_rotator_origin = PolarPoint(25, 0)
    inner_rotator_destination = PolarPoint(1, 100.0 * π)

    # create a couple iterators that will produce a sequence of polar points
    # that spin in lockstep with each other
    for step_counter, (outer_rotator_point, inner_rotator_point) in enumerate(
        iter_no_consectutive_repeats(
            zip(
                iter_linearly_between(
                    outer_rotator_origin, outer_rotator_destination, 2000
                ),
                iter_linearly_between(
                    inner_rotator_origin, inner_rotator_destination, 2000
                ),
            )
        )
    ):
        # add the cartesian origin point with values from the spinning polar points
        current_point = origin_point + outer_rotator_point + inner_rotator_point
        # draw the line segment from prevous and current cartesian points
        a_canvas.draw_successive_line_segment(current_point, step_counter)


a_canvas = Canvas()
looping_spiral(a_canvas)
