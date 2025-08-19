import svg

from devices import Device
from utils import generate_grid


def generate_dayfree(device: Device) -> svg.SVG:
    grid_size = 4.0 * device.mm
    grid_width = int(device.screen_width // grid_size) + 1
    grid_height = int(device.screen_height // grid_size) + 1
    offset_line = 10
    dash_unit = grid_size / 18

    top_corner = (
        (device.screen_width - grid_width * 4.0 * device.mm) / 2,
        (device.screen_height - grid_height * 4.0 * device.mm) / 2,
    )

    return svg.SVG(
        width=device.screen_width,
        height=device.screen_height,
        elements=[
            # border(),
            generate_grid(
                top_corner[0],
                top_corner[1],
                grid_size,
                grid_width,
                grid_height,
                stroke="#888888",
                # stroke_dasharray=[0.375 * MM, 0.25 * MM, 0.375 * MM, 0 * MM],
                # stroke_dasharray=[0.5 * MM, 0.25 * MM, 0.5 * MM, 0 * MM],
                stroke_dasharray=[dash_unit * 2, dash_unit * 2, dash_unit * 2, 0],
            ),
            svg.Path(
                stroke="#000000",
                fill="none",
                stroke_width=2,
                d=[
                    svg.M(
                        x=top_corner[0] + offset_line * grid_size,
                        y=top_corner[1],
                    ),
                    svg.v(grid_size * grid_height),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    print(generate_dayfree(Device.Nomad))
