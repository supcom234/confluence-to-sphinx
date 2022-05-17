import copy
import pdb

from functools import reduce
from ossaudiodev import control_names
from bs4 import NavigableString
from bs4.element import Tag
from confluence_converter.html_util import HTMLTag
from confluence_converter.exporter import ConfluencePage, MyConfluenceExporter
from typing import Dict, Tuple, List, Union
from uuid import uuid4


class InvalidTagError(TypeError):

    def __init__(self, tag: Tag) -> None:
        if tag and tag.name:
            msg = f"Tag {tag.name} is of invalid type."
        else:
            msg = "Tag is None."
        super().__init__(msg)


def make_table(grid: List[List[str]]):
    print(grid)
    cell_width = 2 + max(reduce(lambda x,y: x+y, [[len(item) for item in row] for row in grid], []))
    num_cols = len(grid[0])
    rst = table_div(num_cols, cell_width, 0)
    header_flag = 1
    for row in grid:
        rst = rst + '| ' + '| '.join([normalize_cell(x, cell_width-1) for x in row]) + '|\n'
        rst = rst + table_div(num_cols, cell_width, header_flag)
        header_flag = 0
    return rst

def table_div(num_cols, col_width, header_flag):
    if header_flag == 1:
        return num_cols*('+' + (col_width)*'=') + '+\n'
    else:
        return num_cols*('+' + (col_width)*'-') + '+\n'

def normalize_cell(string, length):
    return string + ((length - len(string)) * ' ')


class CodeBlock:

    def __init__(self, content: str):
        self._content = content

    def indent_content(self, indent=0):
        if indent > 0:
            new_content = []
            for line in self._content.splitlines(True):
                if line == '\n':
                    new_content.append(line)
                else:
                    new_content.append(" " * (indent * 3) + line)
            self._content = ''.join(new_content)

    def __str__(self):
        return self._content


def get_tag_text(tag: Tag, *tags_to_strip) -> str:
    """
    Returns None or a string with values. 
    """
    if tag:
        tag_copy = copy.copy(tag)
        for to_strip in tags_to_strip:
            [x.extract() for x in tag_copy.findAll(to_strip)]

        ret_val = tag_copy.get_text(strip=True).replace('\xa0', ' ')
        if ret_val == '':
            return None

        return ret_val
    return None


class RSTConverter:
    
    def __init__(self, confluence: MyConfluenceExporter = None, link_cache={}, is_confluence_mock=False):
        self._link_cache = link_cache
        self._confluence = confluence
        if is_confluence_mock:
            self._confluence = MyConfluenceExporter()

    def set_page_reference(self, page: ConfluencePage):
        self._page = page

    def _get_image_tag_contents(self, tag: Tag) -> Tuple[Dict, Dict]:
        attachment = tag.find_next("ri:attachment")
        return tag.attrs, attachment.attrs

    def create_image_markup(self, tag: Tag, indent=0) -> Tuple[str, str]:
        """
        .. image:: picture.jpeg
           :height: 100px
           :width: 200 px
           :scale: 50 %
           :alt: alternate text
           :align: right
        :return : image_markup, and filename that needs to be downloaded.
        """
        if tag is None or not HTMLTag.is_image(tag):
            raise InvalidTagError(tag)
        
        image_attrs, attachment_attrs = self._get_image_tag_contents(tag)
        filename = attachment_attrs['ri:filename']
        filename = filename.replace(' ', "\\ ")        
        image_markup = f'\n{" " * 3}.. figure:: /images/{filename}\n'
        if 'ac:height' in image_attrs:
            height = image_attrs['ac:height']
            image_markup = image_markup + f'{" " * 3}   :height: {height}px\n'
        return image_markup, filename

    def create_structured_macro_markup(self, tag: Tag) -> Union[CodeBlock, str]:
        if tag is None or not HTMLTag.is_structured_macro(tag):
            raise InvalidTagError(tag)

        if tag.attrs and tag.attrs['ac:name'] == "note":
            return self.create_code_block(get_tag_text(tag))
        elif tag.attrs and tag.attrs['ac:name'] == "code":
            tag = tag.find_next("ac:plain-text-body")
            return self.create_code_block(get_tag_text(tag))
        elif tag.attrs and tag.attrs['ac:name'] == "anchor":
            anchor_id = str(uuid4())[0:8]
            self._link_cache[tag.string.strip()] = anchor_id
            return f".. _{anchor_id}:\n"
        elif HTMLTag.has_rich_text_body(tag):
            return self.create_code_block(get_tag_text(tag))

    def _create_list_data_struct(self, tag: Tag) -> List:
        list_items = tag.find_all("li", recursive=False)
        list_data_struct = []
        for list_item in list_items:
            # text = get_tag_text(list_item, "ol", "ul", "ac:structured-macro")
            # if text != None:
            #     list_data_struct.append(text)
            # if list_item.string:
            #     list_data_struct.append(list_item.string)

            for child in list_item.children:
                if HTMLTag.is_structured_macro(child):
                    list_data_struct.append(self.create_structured_macro_markup(child))
                elif HTMLTag.is_image(child):
                    markup, filename = self.create_image_markup(child)
                    self._confluence.download_image(filename, self._page)
                    list_data_struct.append(CodeBlock(markup))
                elif HTMLTag.is_paragraph(child):
                    list_data_struct.append(self.create_paragraph_markup(child))
                elif HTMLTag.is_ordered_list(child):
                    list_data_struct.append(self._create_list_data_struct(child))
                elif HTMLTag.is_unordered_list(child):
                    list_data_struct.append(self._create_list_data_struct(child))
                elif isinstance(child, NavigableString):
                    list_data_struct.append(self._my_string(child))

        return list_data_struct

    def _create_list(self, content: List[Union[str, List, CodeBlock]], indent=0, output="") -> str:
        output += "\n"
        count = 1
        for item in content:
            if isinstance(item, list):                
                output = self._create_list(item, indent+1, output)
            elif isinstance(item, CodeBlock):
                item.indent_content(indent)
                #the_string = " " * (indent * 3) + str(item)
                output += str(item)#the_string
            elif isinstance(item, str):
                the_string = f"{count}. {item}\n"
                the_string = " " * (indent * 3) + the_string
                output += the_string
                count += 1
            else:
                raise ValueError("Invalid data structure.")
        return output

    def create_list_markup(self, tag: Tag) -> str:
        if tag is None or not (HTMLTag.is_ordered_list(tag) or HTMLTag.is_unordered_list(tag)):
            raise InvalidTagError(tag)
            
        data_struct = self._create_list_data_struct(tag)
        # pdb.set_trace()
        return self._create_list(data_struct)

    def create_code_block(self, content: str) -> CodeBlock:
        if content != None and len(content) > 0:
            new_content = []
            for line in content.splitlines():
                new_content.append((" " * 3) + line)

            new_content = '\n'.join(new_content).rstrip()
            return CodeBlock(f"\n::\n\n{new_content}\n\n")

    def create_heading_markup(self, tag: Tag) -> str:
        if tag is None or tag.text is None or not HTMLTag.is_heading(tag):
            raise InvalidTagError(tag)
                
        my_string = tag.text.strip()
        if len(my_string) == 0:
            return ''
        if tag.name == "h1":
            my_char = "-"
        elif tag.name == "h2":
            my_char = "^"
        elif tag.name == "h3":
            my_char = ":"
        elif tag.name == "h4":
            my_char = ";"

        return f"\n{my_string}\n{my_char * len(my_string)}\n\n"

    def _my_string(self, tag: Tag) -> str:
        my_string = ""
        if tag.string:
            my_string = tag.string.strip()    
        elif isinstance(tag.next, NavigableString):
            my_string = tag.next.string.strip()
        return my_string

    def create_link_markup(self, tag: Tag) -> str:
        if tag is None or not HTMLTag.is_link(tag):
            raise InvalidTagError(tag)

        ret_val = ""
        if "ac:anchor" in tag.attrs:
            title = tag.attrs['ac:anchor']
            if title in self._link_cache:
                anchor_label = self._link_cache[title]
                ret_val = f":ref:`{title} <{anchor_label}>`"
        elif "href" in tag.attrs:
            link = tag.attrs["href"]
            if tag.next:
                ret_val = link if link == str(tag.next) else f"`{str(tag.next)} <{link}>`_"
            else:
                ret_val = link
        return ret_val

    def _handle_paragraph_markup(self, tag: Tag, ret_val: str="") -> str:
        if HTMLTag.is_paragraph(tag) or HTMLTag.is_underline(tag):
            my_string = self._my_string(tag)
            ret_val = ret_val + " " + my_string
        elif HTMLTag.is_strong(tag):
            my_string = self._my_string(tag)
            ret_val = ret_val + f" **{my_string}**"
        elif HTMLTag.is_italics(tag):                
            my_string = self._my_string(tag)
            ret_val = ret_val + f" *{my_string}*"
        elif HTMLTag.is_link(tag):
            ret_val = self.create_link_markup(tag)
        elif HTMLTag.is_image(tag):
            ret_val, filename = self.create_image_markup(tag)
            self._confluence.download_image(filename, self._page)
        # elif tag.next is not None and isinstance(tag.next, NavigableString):
        #     my_string = self._my_string(tag)
        #     ret_val = ret_val + " " + my_string

        return ret_val

    def create_paragraph_markup(self, tag: Tag) -> str:
        ret_val = ""
        if HTMLTag.is_parent_a_macro_or_rich_text(tag):
            return ret_val
        
        ret_val = self._handle_paragraph_markup(tag)
        for child in tag.children:
            ret_val = self._handle_paragraph_markup(child, ret_val)
            
        ret_val = ret_val.replace('\xa0', ' ')
        ret_val = ret_val + "\n"
        ret_val = ret_val.lstrip()
        return ret_val

def main():
    c = RSTConverter()
    # s = ["Item one", "Item two", ["Subitem one", "Subitem two", ["subsub item one"] ]]
    # output = ""
    # print(c.create_list(s))
    t = 'def transform(self):\n    self._create_top_level_heading(self._page_title)\n    for tag in self._soup.find_all(recursive=False): #type: Tag\n        self._process_tag(tag)\n        self._lines.append("\\n")\n        with open("sphinx/pages/mytest.rst", "w") as f:\n            f.writelines(self._lines)'
    print(c.create_code_block(t))
    
    

if __name__ == '__main__':
    main()