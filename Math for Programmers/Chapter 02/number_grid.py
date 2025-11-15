from manim import *

__all__ = ["NumberGrid"]

class NumberGrid():
    def __init__(self, xmin, xmax, xstep, ymin, ymax, ystep, include_tips=False):
            aspect = config.pixel_width / config.pixel_height
            config.frame_height = config.frame_width / aspect
            
            grid = NumberPlane(
                x_range=[xmin, xmax, xstep],
                y_range=[ymin, ymax, ystep],
                x_length=config.frame_width  - 2,
                y_length=config.frame_height - 2,
                x_axis_config={
                    "include_numbers": True,
                    "numbers_to_exclude": (),
                    "numbers_to_include": np.arange(xmin, xmax + 1, xstep),
                    "label_direction": ORIGIN,
                    "font_size": 36,
                    "stroke_width": 3,
                    "include_tip": include_tips,
                },
                y_axis_config={
                    "include_numbers": True,
                    "numbers_to_exclude": (),
                    "numbers_to_include": np.arange(ymin, ymax + 1, ystep),
                    "label_direction": ORIGIN,
                    "font_size": 36,
                    "stroke_width": 3,
                    "include_tip": include_tips,
                },
            )

            # corners of the grid in scene coordinates
            lower_left = grid.c2p(xmin, ymin)
            upper_right = grid.c2p(xmax, ymax)

            # center + size from those corners
            center = (lower_left + upper_right) / 2
            width = abs(upper_right[0] - lower_left[0])
            height = abs(upper_right[1] - lower_left[1])

            edge = Rectangle(
                width=width,
                height=height,
                stroke_color=WHITE,
                stroke_width=2,
            ).move_to(center)

            left_x = grid.get_edge_center(LEFT)[0]
            bottom_y = grid.get_edge_center(DOWN)[1]

            vpad = 0.4
            hpad = 0.2

            x_nums = grid.x_axis.numbers
            y_nums = grid.y_axis.numbers

            x_nums.set_y(bottom_y - vpad)
            y_nums.set_x(left_x- hpad)

            def create_ticks(bottom_ticks, left_ticks):
                tick_length = 0.15
                tick_stroke = 2

                # x-axis ticks placed along the bottom border
                for v in np.arange(xmin, xmax + 1, xstep):
                    pt = grid.c2p(v, ymin)
                    tick = Line(
                        pt,
                        pt + tick_length * DOWN,
                        stroke_width=tick_stroke
                    )
                    bottom_ticks.add(tick)

                # y-axis ticks placed along the left border
                for v in np.arange(ymin, ymax + 1, ystep):
                    pt = grid.c2p(xmin, v)
                    tick = Line(
                        pt,
                        pt + tick_length * LEFT,
                        stroke_width=tick_stroke
                    )
                    left_ticks.add(tick)

            bottom_ticks = VGroup()
            left_ticks   = VGroup()
            create_ticks(bottom_ticks, left_ticks)

            offset = 0.3

            group = VGroup(grid, edge, bottom_ticks, left_ticks, x_nums, y_nums)
            group.shift(offset * UP + offset * RIGHT)

            self.group = group
            self.grid = grid
            self.edge = edge
            self.bottom_ticks = bottom_ticks
            self.left_ticks = left_ticks
            self.x_nums = x_nums
            self.y_nums = y_nums