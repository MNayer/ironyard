from PIL import Image
from PIL.ImageFile import ImageFile
from tempfile import TemporaryDirectory
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from subprocess import run
from typing import List
from datetime import date

from db import PublicationUpdate


def do_run(cmd):
    run(cmd, capture_output=True, check=True)


def render_typst(typst: str) -> ImageFile:
    with TemporaryDirectory() as dir:
        temp_path = Path(dir)
        typst_path = temp_path / "source.typ"
        image_path = temp_path / "image.png"

        typst_path.write_text(typst)

        cmd = f"typst compile -f png {str(typst_path)} {str(image_path)}"
        do_run(cmd.split())

        image = Image.open(image_path)

    return image


def render_new_publications(publications: List[PublicationUpdate]) -> List[ImageFile]:
    env = Environment(loader=FileSystemLoader("./templates/"))
    template = env.get_template("new.typ")

    images = []
    total_publications = len(publications)
    multiple_publications = total_publications > 1

    for idx, publication in enumerate(publications, start=1):
        author = ", ".join(publication.authors)
        typst = template.render(
            title=publication.title,
            author=author,
            multiple_publications=multiple_publications,
            current_publication=idx,
            total_publications=total_publications,
        )
        image = render_typst(typst)
        images.append(image)

    return images


def render_default() -> ImageFile:
    env = Environment(loader=FileSystemLoader("./templates/"))
    template = env.get_template("default.typ")

    cd = date.today()
    date_str = f"{cd:%A}, {cd:%-d}.{cd:%-m}.{cd:%Y}"

    typst = template.render(date=date_str)
    image = render_typst(typst)

    return image
