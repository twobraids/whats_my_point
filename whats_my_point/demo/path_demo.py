#!/usr/bin/env python3.10

# WARNING - this script makes almost 100 images for assembly into a video

from math import pi as π
from PIL import Image, ImageDraw
from more_itertools import windowed

from whats_my_point import (
    CartesianPoint,
    PolarPoint,
    iter_linear_steps_between,
    iter_natural_steps_between,
    Path,
)


class Canvas:
    # wrap the drawable image with a quicky interface to make the demo code look simpler.
    def __init__(self):
        self.the_image = Image.new("RGB", (600, 600), (0, 0, 0))
        self.the_drawable_image = ImageDraw.Draw(self.the_image)
        self.image_counter = 0
        self.previous_point = None
        self.step_counter = 0

    def draw_line_segment(self, start_point, end_point):
        cartesian_start_point = CartesianPoint(start_point)
        cartesian_end_point = CartesianPoint(end_point)
        self.the_drawable_image.line(
            (cartesian_start_point, cartesian_end_point),
            fill="rgb(0, 255, 0)",
            width=3,
        )
        if not (self.step_counter % 9):
            self.the_image.save(f"./path_demo_{self.image_counter:04d}.png")
            self.image_counter += 1
        self.step_counter += 1


def draw_path_demo(a_canvas):
    """Draw 9 looping rays from the center of the canvas"""

    canvas_middle_point = CartesianPoint(a_canvas.the_image.size) / 2

    collection_of_ray_paths = []

    # materialize a spiral path of PolarPoints about the origin
    spiral_path = Path(
        iter_natural_steps_between(PolarPoint(0, 0), PolarPoint(50, 10 * π), 100)
    )

    for θ in iter_linear_steps_between(0, 2 * π, 9):

        # materialize a path of PolarPoints making a straight ray from the origin
        ray_path = Path(
            iter_linear_steps_between(PolarPoint(0, θ), PolarPoint(300, θ), 100)
        )

        # combine the straight rays with the spiral path and translate them
        # from the canvas origin to the canvas middle - save the result as
        # a path of PolarPoints
        collection_of_ray_paths.append(ray_path + spiral_path + canvas_middle_point)

    # set up windowing iterators for all the spiraling ray paths
    windowed_iter_for_every_ray_path = (
        windowed(a_ray_path, 2) for a_ray_path in collection_of_ray_paths
    )

    # step through the all the spiral ray paths in parallel, round robin style
    for a_segment_for_every_ray in zip(*windowed_iter_for_every_ray_path):
        for start_point, end_point in a_segment_for_every_ray:
            a_canvas.draw_line_segment(start_point, end_point)


a_canvas = Canvas()
draw_path_demo(a_canvas)
