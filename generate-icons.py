import os
from collections.abc import Iterable
from pathlib import Path

import click
from PIL import Image


@click.command()
@click.option(
    "--dir",
    default=Path.home() / "steam/steamapps/common/Factorio",
    type=click.Path(path_type=Path),
    help="Factorio installation directory",
)
@click.option(
    "--out",
    default="generated",
    type=click.Path(path_type=Path, exists=False),
    help="Output directory",
)
def main(dir: Path, out: Path):
    print("Hello from factorio-icons!")
    print(f"Using {dir}, output {out.resolve()}")
    out.mkdir(parents=True, exist_ok=True)
    for idir in icon_dirs(dir):
        process_icon_dir(idir, out)


def icon_dirs(dir: Path) -> Iterable[Path]:
    for entry in (dir / "data").glob("*"):
        icon_dir = entry / "graphics/icons"
        if icon_dir.exists():
            yield icon_dir


def write(img: Image, out: Path, category: str, fname: Path, x: int, w: int):
    name = fname.stem
    new_img = img.crop((x, 0, x + w, w))
    out_fname = out / f"Factorio.{name}.{category}.{w}.png"
    print(out_fname)
    new_img.save(out_fname)


def process_icon_dir(dir: Path, out: Path):
    category = dir.parts[-3]
    print(f"Processing {category}, dir={dir}")

    for fname in dir.glob("*.png"):
        img = Image.open(fname)
        write(img, out, category, fname, 0, 64)
        write(img, out, category, fname, 64, 32)
        write(img, out, category, fname, 96, 16)


if __name__ == "__main__":
    main()
