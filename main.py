import argparse
from collections.abc import Callable
from functools import partial
from pathlib import Path
import subprocess

import svg

from devices import Device
import page_4mm_dot_grid
import page_5mm_dot_grid
import page_daily_planner
import page_dayfree
import page_isometric
import page_ruled_line



PAGES = {
    "page_4mm_dot_grid": page_4mm_dot_grid.generate_4mm_dot_grid,
    "page_isometric": page_isometric.generate_isometic_grid,
    "page_5mm_dot_grid": page_5mm_dot_grid.generate_5mm_dot_grid,
    "page_daily_planner": page_daily_planner.generate_daily_planner,
    "page_dayfree": page_dayfree.generate_dayfree,
    "page_6mm_ruled_line": partial(page_ruled_line.generate_ruled_line, spacing=6)
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
    parser.add_argument("--output", "-o", choices=["svg", "png", "both"], help="Output file type")
    args = parser.parse_args()
    templates = get_templates(args.template)
    device = args.device
    for template in templates:
        generate_function = PAGES[template]
        base_file = Path("out") / f"{template}_{device}"
        create_svg(generate_function, device, base_file)
        ext = "svg"
        if args.output in {"png", "both"}:
            try:
                create_png(base_file)
            except FileNotFoundError:
                print("Could not create png, inkscape is not in the PATH.")
            else:
                if args.output == "png":
                    base_file.with_suffix(".svg").unlink()
                    ext = "png"
                else:
                    ext = "svg & png"
        print(f"Created {base_file} {ext}")


def create_svg(func: Callable[[Device], svg.SVG], device: Device, base_file: Path) -> None:
    contents = func(device)
    with base_file.with_suffix(".svg").open("w") as f:
        f.write(str(contents))


def create_png(base_file: Path) -> None:
    subprocess.run(
        [
            "inkscape",
            str(base_file.with_suffix(".svg")),
            "-o",
            str(base_file.with_suffix(".png")),
            "-b",
            "white",
            "--export-png-color-mode=Gray_16",
        ],
        check=True,
    )


def get_templates(template: str) -> list[str]:
    templates = list(PAGES.keys())
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
