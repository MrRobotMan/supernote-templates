import svg

from devices import Device
from utils import generate_dot_grid


def generate_5mm_dot_grid(device: Device) -> svg.SVG:
    grid_size = 5.0 * device.mm
    grid_width = int(device.screen_width // grid_size)
    grid_height = int(device.screen_height // grid_size)

    top_corner = (
        (device.screen_width - grid_width * grid_size) / 2,
        (device.screen_height - grid_height * grid_size) / 2,
    )

    return svg.SVG(
        width=device.screen_width,
        height=device.screen_height,
        elements=[
            # border(),
            generate_dot_grid(
                top_corner[0],
                top_corner[1],
                grid_size,
                grid_width,
                grid_height,
                fill="#888888",
            ),
        ],
    )


if __name__ == "__main__":
    print(generate_5mm_dot_grid(Device.Nomad))
