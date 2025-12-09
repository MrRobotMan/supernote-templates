from svg import SVG, Line

from devices import Device

def generate_ruled_line(device: Device, spacing: float) -> SVG:
    start = 9 * device.mm
    end = device.screen_width - 9 * device.mm
    y_offset = 11*device.mm
    spacing = spacing * device.mm
    lines = int((device.screen_height - y_offset )/spacing)

    def make_line(row: int) -> Line:
       return Line(stroke="#888888", stroke_width=1, x1=start, x2=end, y1=y_offset +spacing*row, y2=y_offset+spacing*row )

    return SVG(
        width=device.screen_width,
        height=device.screen_height,
        elements=[make_line(n) for n in range(lines)]    
    )



