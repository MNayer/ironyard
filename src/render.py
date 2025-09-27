from PIL import Image
from PIL.ImageFile import ImageFile
from tempfile import TemporaryDirectory
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from subprocess import run
from typing import List


def do_run(cmd):
    res = run(cmd, capture_output=True, check=True)
    print(res)


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


def render_new_publications(publications: dict) -> List[ImageFile]:
    env = Environment(loader=FileSystemLoader("./templates/"))
    template = env.get_template("new.typ")

    images = []
    total_publications = len(publications)
    multiple_publications = total_publications > 1

    for idx, (title, author) in enumerate(publications.items(), start=1):
        author = ", ".join(author)
        typst = template.render(
            title=title,
            author=author,
            multiple_publications=multiple_publications,
            current_publication=idx,
            total_publications=total_publications,
        )
        image = render_typst(typst)
        images.append(image)

    return images
