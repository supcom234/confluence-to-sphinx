from confluence_converter import JINJA_DIR, PROJECT_ROOT_DIR
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List

JINJA_ENV = Environment(
    loader=FileSystemLoader(str(JINJA_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)

def generate_index_rst_file(pages: List):
    template = JINJA_ENV.get_template("index.rst.j2")
    index_template = template.render(pages=pages)

    with open(PROJECT_ROOT_DIR + "/sphinx/index.rst", "w") as fhandle:
        fhandle.write(index_template)