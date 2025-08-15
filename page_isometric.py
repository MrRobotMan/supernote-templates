import math

import svg

import utils
from devices import Device


def generate_isometic_grid(device: Device) -> svg.SVG:
    angle = math.pi / 6  # 30 degrees
    grid_size_vertical = 4.0 * device.mm
    grid_size_horizontal = grid_size_vertical / (2 * math.tan(angle))
    grid_cols = int(device.screen_width // grid_size_horizontal)
    grid_rows = int(device.screen_height // grid_size_vertical)

    x_start = (device.screen_width - grid_cols * grid_size_horizontal) / 2
    y_start = (device.screen_height - grid_rows * grid_size_vertical) / 2

    return svg.SVG(
        width=device.screen_width,
        height=device.screen_height,
        elements=[
            utils.generate_angled_grid(
                (x_start, y_start),
                (grid_size_horizontal, grid_size_vertical),
                (grid_rows, grid_cols),
                angle,
                fill="#888888",
            ),
        ],
    )


if __name__ == "__main__":
    generate_isometic_grid(Device.Nomad)
