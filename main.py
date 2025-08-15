import argparse
import subprocess
from collections.abc import Callable
from pathlib import Path

import svg

import page_4mm_dot_grid
import page_isometric
from devices import Device

# import page_5mm_dot_grid
# import page_daily_planner
# import page_dayfree

PAGES = {
    "page_4mm_dot_grid": page_4mm_dot_grid.generate_4mm_dot_grid,
    "page_isometric": page_isometric.generate_isometic_grid,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Digital Notebook Template Generator",
        description="Generate background templates for digital notebooks from Supernote and Remarkable",
    )
    parser.add_argument("template", help="Name of the template to generate or 'ALL'")
    parser.add_argument(
        "device",
        choices=["nomad", "manta", "remarkable2"],
        type=Device,
        help="Device to generate the template for.",
    )
    parser.add_argument(
        "--output", "-o", choices=["svg", "png"], default="svg", help="Output file type"
    )
    args = parser.parse_args()
    templates = get_templates(args.template)
    device = args.device
    for template in templates:
        generate_function = PAGES[template]
        base_file = Path("out") / f"{template}_{device}"
        create_svg(generate_function, device, base_file)
        if args.output == "png":
            create_png(base_file)
            base_file.with_suffix(".svg").unlink()
        print(f"Created {base_file}")


def create_svg(
    func: Callable[[Device], svg.SVG], device: Device, base_file: Path
) -> None:
    contents = func(device)
    with base_file.with_suffix(".svg").open("w") as f:
        f.write(str(contents))


def create_png(base_file: Path) -> None:
    subprocess.run(
        [
            "inkscape",
            str(base_file.with_suffix(".svg")),
            str(base_file.with_suffix(".png")),
            "-b",
            "white",
            "--export-png-color-mode=Gray_16",
        ]
    )


def get_templates(template: str) -> list[str]:
    templates = [p.stem for p in Path().iterdir() if p.stem.startswith("page_")]
    if template.lower() == "all":
        return templates
    if not template.startswith("page"):
        template = f"page_{template}"
    template.removesuffix(".py")
    if template not in templates:
        print(f"Invalid template {template}")
        return []
    return [template]


if __name__ == "__main__":
    main()
