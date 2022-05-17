import shutil

from bs4 import BeautifulSoup
from bs4.element import Tag
from confluence_converter import SPHINX_PAGES_DIR, SPHINX_IMAGES_DIR
from confluence_converter.config_util import ConfigManager
from confluence_converter.html_util import HTMLTag
from confluence_converter.exporter import MyConfluenceExporter, ConfluencePage
from confluence_converter.rst_converter import make_table, RSTConverter
from confluence_converter.jinja_util import generate_index_rst_file
from pathlib import Path


def print_tag(tag: Tag):
    if isinstance(tag, Tag):
        print(f"TAG: {tag}")
        print(f"TAG STRING: {tag.string}")
        print(f"TAG NAME: {tag.name}") #type: Tag
        print(f"TAG ATTRS: {tag.attrs}")
        print(type(tag))
        children = len(tag.find_all())
        print(f"Children: {children}")
    else:        
        print(tag)
        print(type(tag))
    print()


class ConfluenceTransformer:

    def __init__(self, config: ConfigManager):
        self._config = config
        self._exporter = MyConfluenceExporter(self._config)
        self._lines = []
        self._hash_dict = {}          
        self._rst_converter = RSTConverter(confluence=self._exporter)
    
    def _add_string(self, the_string: str):
        if the_string and len(the_string) > 0:
            print("APPENDING: " + the_string)
            self._lines.append(the_string)

    def _create_top_level_heading(self, some_str: str):
        self._add_string(some_str + "\n")
        line = "=" * len(some_str)
        self._add_string(line + "\n")   

    def _has_children(self, tag: Tag) -> bool:
        if isinstance(tag, Tag):
            children = len(tag.find_all())
            return children > 0
        return False    

    def _create_table_markup(self, tag: Tag):
        if tag.name == "table":
            grid = []
            for row in tag.find_all("tr"):
                # if self._has_children(row):
                row_list = []
                for child in row.children:
                    if child.name == "th" or child.name == "td":
                        if child and child.text:
                            row_list.append(child.text.strip())
                grid.append(row_list)

            self._add_string(make_table(grid) + "\n")

    def _process_tag(self, tag: Tag, page: ConfluencePage, indent=0):
        print_tag(tag)        
        if HTMLTag.is_heading(tag):
            value = self._rst_converter.create_heading_markup(tag)
            self._add_string(value)
        elif HTMLTag.is_paragraph(tag) or HTMLTag.is_span(tag) or HTMLTag.is_strong(tag):
            self._add_string(self._rst_converter.create_paragraph_markup(tag))            
        elif HTMLTag.is_structured_macro(tag):
            self._add_string(str(self._rst_converter.create_structured_macro_markup(tag)))
        elif HTMLTag.is_break(tag):
            self._add_string("\n")
        elif HTMLTag.is_image(tag):
            markup, filename = self._rst_converter.create_image_markup(tag)
            self._download_image(filename, page)
            self._add_string(markup)
        elif HTMLTag.is_ordered_list(tag) or HTMLTag.is_unordered_list(tag):
            self._add_string(self._rst_converter.create_list_markup(tag))
        elif HTMLTag.is_table(tag):
            self._create_table_markup(tag)
        elif HTMLTag.is_link(tag):
            self._add_string(self._rst_converter.create_link_markup(tag))

    def _clean_previous_run(self):
        for directory in [SPHINX_PAGES_DIR, SPHINX_IMAGES_DIR]:
            shutil.rmtree(directory)
            Path(directory).mkdir(parents=True)

    def transform(self):
        page_titles = []
        self._clean_previous_run()
        for page in self._exporter.page_iterator(): # type: ConfluencePage
            self._rst_converter.set_page_reference(page)
            self._create_top_level_heading(page.title)
            markup = BeautifulSoup(page.content_body, "html.parser")
            for tag in markup.find_all(recursive=False): #type: Tag
                self._process_tag(tag, page)
                self._add_string("\n")

            with open(f"sphinx/pages/{page.title_filename}.rst", "w") as f:
                f.writelines(self._lines)

            page_titles.append(page.title_filename)
        generate_index_rst_file(page_titles)


def main():    
    args = ConfigManager.setup_arg_parse_options()
    config = ConfigManager(args)
    transformer = ConfluenceTransformer(config)
    transformer.transform()
    

if __name__ == '__main__':
    main()