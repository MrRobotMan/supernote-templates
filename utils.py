from collections.abc import Callable
from math import tan, atan, pi
from typing import Any

import svg


def generate_grid(
    x: float,
    y: float,
    size: float,
    width: int,
    height: int,
    enable_border: bool = True,
    stroke: str = "#000000",
    stroke_width: int = 1,
    **kwargs: Any,
):
    elements: list[svg.Element] = []

    start = 0 if enable_border else 1
    end_offset = 1 if enable_border else 0

    for x_pos in range(start, width + end_offset):
        elements.append(
            svg.Path(
                stroke=stroke,
                stroke_width=stroke_width,
                d=[
                    svg.M(x + x_pos * size, y),
                    svg.v(size * height),
                ],
                **kwargs,
            )
        )

    for y_pos in range(start, height + end_offset):
        elements.append(
            svg.Path(
                stroke=stroke,
                stroke_width=stroke_width,
                d=[
                    svg.M(x, y + y_pos * size),
                    svg.h(size * width),
                ],
                **kwargs,
            )
        )

    return svg.G(
        fill="none",
        elements=elements,
    )


def generate_dot_grid(
    x: float, y: float, size: float, width: int, height: int, fill: str = "#000000"
):
    elements: list[svg.Element] = []

    for x_pos in range(width + 1):
        for y_pos in range(height + 1):
            elements.append(
                svg.Circle(
                    fill=fill,
                    cx=x + x_pos * size,
                    cy=y + y_pos * size,
                    r=2,
                )
            )

    return svg.G(
        fill="none",
        elements=elements,
    )


def generate_angled_grid(
    start_point: tuple[float, float],
    step: tuple[float, float],
    size: tuple[int, int],
    angle: float,
    border: Callable[[], svg.Element] | None = None,
    stroke: str = "#000000",
    stroke_width: int = 1,
    **kwargs: Any,
):
    elements: list[svg.Element] = []
    (x_start, y_start) = start_point
    (x_step, y_step) = step
    (rows, cols) = size
    width = x_step * cols
    height = y_step * rows

    if border:
        elements.append(border())
        end_offset = 0
    else:
        end_offset = 1

    # Vertical Lines, angled lines down across top and angled lines up across bottom
    for x_pos in range(cols + end_offset):
        if not border or x_pos > 0:
            elements.append(
                svg.Path(
                    stroke=stroke,
                    stroke_width=stroke_width,
                    d=[svg.M(x_start + x_pos * x_step, y_start), svg.v(height)],
                    **kwargs,
                )
            )
        if x_pos % 2 == 0 and x_pos < cols:
            x_pos = x_start + x_pos * x_step
            dy = (x_start + width - x_pos) * tan(angle)
            if dy > height:
                y_pos_dn = y_start + height
                y_pos_up = y_start
                x_end = x_pos + height / tan(angle)
            else:
                y_pos_up = y_start + height - dy
                y_pos_dn = y_start + dy
                x_end = x_start + width
            # Angled up
            elements.append(
                svg.Path(
                    stroke=stroke,
                    stroke_width=stroke_width,
                    d=[svg.M(x_pos, y_start + height), svg.L(x_end, y_pos_up)],
                    **kwargs,
                )
            )

            # Angled down
            elements.append(
                svg.Path(
                    stroke=stroke,
                    stroke_width=stroke_width,
                    d=[svg.M(x_pos, y_start), svg.L(x_end, y_pos_dn)],
                    **kwargs,
                )
            )

    # Move down the left side
    for y_pos in range(1, rows):
        dy = y_pos * y_step

        dx_up = dy / tan(angle)
        if dx_up > width:
            y_end_up = y_start + (dx_up - width) * tan(angle)
            x_end_up = x_start + width
        else:
            y_end_up = y_start
            x_end_up = x_start + dx_up

        dx_dn = (height - dy) / tan(angle)
        if dx_dn > width:
            y_end_dn = y_start + height - (dx_dn - width) * tan(angle)
            x_end_dn = x_start + width
        else:
            y_end_dn = y_start + height
            x_end_dn = x_start + dx_dn

        # Lines angled up
        elements.append(
            svg.Path(
                stroke=stroke,
                stroke_width=stroke_width,
                d=[svg.M(x_start, y_start + dy), svg.L(x_end_up, y_end_up)],
                **kwargs,
            )
        )

        # Lines angled down
        elements.append(
            svg.Path(
                stroke=stroke,
                stroke_width=stroke_width,
                d=[svg.M(x_start, y_start + dy), svg.L(x_end_dn, y_end_dn)],
                **kwargs,
            )
        )

    return svg.G(
        fill="none",
        elements=elements,
    )
