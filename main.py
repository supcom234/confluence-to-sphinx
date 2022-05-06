import copy
import os
import json
import hashlib
import re
import pdb

from uuid import uuid4
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from pathlib import Path
from confluence_converter.exporter import MyConfluenceExporter
from confluence_converter.rst_converter import CodeBlock, make_table, RSTConverter
from typing import List, Tuple, Dict, Union


CONFLUENCE_URL = "https://confluence.di2e.net"
# CONFLUENCE_USERNAME = "zTHISISCVAH"
# CONFLUENCE_PASSWORD = "We.are.tfplenum4$$$"

CONFLUENCE_USERNAME = "david.navarro"
CONFLUENCE_PASSWORD = ""
CONFLUENCE_SPACE = "THISISCVAH"
CONFLUENCE_SAMPLE = "v3.7 Deployable Interceptor Platform (DIP) Troubleshooting Guide"
# CONFLUENCE_SAMPLE = "Test Page Delete Later For prototype"

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def print_tag(tag: Tag):
    if isinstance(tag, Tag):
        print(f"TAG: {tag}")
        # if "This is a test2" in str(tag):
        #     pdb.set_trace()
        
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


def print_json(somedict: Union[Dict, List]):
    print(json.dumps(somedict, indent=4, sort_keys=True))
    print(type(somedict))


# def get_tag_string(tag: Tag) -> str:
#     if tag and tag.string:
#         my_string = tag.string.strip()
#         if len(my_string) > 0:
#             return my_string
#     return ""

def get_tag_text(tag: Tag, *tags_to_strip) -> str:
    """
    Returns None or a string with values. 
    """
    if tag:
        tag_copy = copy.copy(tag)
        for to_strip in tags_to_strip:
            [x.extract() for x in tag_copy.findAll(to_strip)]

        ret_val = tag_copy.get_text(strip=True).replace('\xa0', ' ')
        # if "directory" in ret_val:
        #     # import pdb
        #     pdb.set_trace()
        if ret_val == '':
            return None

        return ret_val
    return None

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def get_tag_textv2() -> str:    
    raw_html = '<ac:structured-macro ac:macro-id="6f3108bc-479e-43fe-80b6-e2c36d042b60" ac:name="note" ac:schema-version="1"><ac:rich-text-body><p>Screenshots will be saved to the<strong>\xa0</strong>Pictures<strong>\xa0</strong>directory in the current user\'s home directory.</p></ac:rich-text-body></ac:structured-macro>'
    raw_html = raw_html.replace("<strong>", "**")
    raw_html = raw_html.replace("</strong>", "**")
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


class ConfluenceTransformer:

    def __init__(self, page_title: str):
        self._confluence = MyConfluenceExporter(url=CONFLUENCE_URL,
                                                username=CONFLUENCE_USERNAME,
                                                password=CONFLUENCE_PASSWORD)
        print(page_title)         
        page_id = self._confluence.get_page_id(CONFLUENCE_SPACE, page_title)
        page = self._confluence.get_page_by_id(page_id, expand="body.storage")
        attachments = self._confluence.get_attachments_from_content(page_id)
        
        self._page_title = page_title
        self._content = page['body']['storage']['value']
        self._soup = BeautifulSoup(self._content, "html.parser")
        self._lines = []
        self._hash_dict = {}
        self._link_cache = {}
        self._attachments = attachments
        self._rst_converter = RSTConverter()
    
    def _create_top_level_heading(self, some_str: str):
        self._lines.append(some_str + "\n")
        line = "=" * len(some_str)
        self._lines.append(line + "\n")

    def _add_hash(self, some_str: str):
        self._hash_dict[hashlib.md5(some_str.encode('utf-8')).hexdigest()] = True

    def _add_string(self, the_string: str):
        if the_string and len(the_string) > 0:
            # if not self._is_dupicate(the_string):
            self._lines.append(the_string)
                # self._add_hash(the_string)

    def _is_tag(self, tag: Tag, tag_type: str) -> bool:
        if not isinstance(tag, Tag):
            return False
        return tag.name == tag_type

    def _is_paragraph_tag(self, tag: Tag) -> bool:
        if self._has_structured_macro_tag(tag):
            return False
        return self._is_tag(tag, "p")

    def _is_structured_macro_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "ac:structured-macro")

    def _is_rich_text_body_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "ac:rich-text-body")

    def _is_heading_tag(self, tag: Tag) -> bool:
        if self._is_tag(tag, "h1") or self._is_tag(tag, "h2") or self._is_tag(tag, "h3") or self._is_tag(tag, "h4"):
            return True
        return False

    def _is_span_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "span")

    def _is_strong_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "strong")
        
    def _is_break_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "br")

    def _is_table_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "table")

    def _is_ordered_list_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "ol")

    def _is_unordered_list_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "ul")

    def _is_image_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "ac:image")
    
    def _is_link_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "ac:link")

    def _is_list_item_tag(self, tag: Tag) -> bool:
        return self._is_tag(tag, "li")

    def _get_image_tag_contents(self, tag: Tag) -> Tuple[Dict, Dict]:
        if tag.name != "ac:image":
            raise Exception("Not an ac:image tag.")

        attachment = tag.find_next("ri:attachment")
        return tag.attrs, attachment.attrs
        
    def _has_tag(self, tag: Tag, tag_name: str) -> bool:
        if not isinstance(tag, Tag):
            return False
        
        for child_tag in tag:
            if child_tag.name == tag_name:
                return True

        return False

    def _has_children(self, tag: Tag) -> bool:
        if isinstance(tag, Tag):
            children = len(tag.find_all())
            return children > 0
        return False

    def _has_structured_macro_tag(self, tag: Tag) -> bool:
        return self._has_tag(tag, "ac:structured-macro")

    def _has_rich_text_body_tag(self, tag: Tag) -> bool:
        return self._has_tag(tag, "ac:rich-text-body")
    
    def _download_image(self, filename: str):
        for item in self._attachments['results']:
            if item["title"] == filename:
                item["_links"]["download"]
                self._confluence.download_attachement(CONFLUENCE_URL + item["_links"]["download"], SCRIPT_DIR + "/sphinx/images/" + filename)

    def _create_image_markup(self, tag: Tag, indent=0) -> str:
        """
        .. image:: picture.jpeg
           :height: 100px
           :width: 200 px
           :scale: 50 %
           :alt: alternate text
           :align: right        
        """
        print("Creating Image tag")        
        image_attrs, attachment_attrs = self._get_image_tag_contents(tag)
        filename = attachment_attrs['ri:filename']
        self._download_image(filename)
        filename = filename.replace(' ', "\\ ")        
        image_markup = f'\n{" " * 3}.. figure:: /images/{filename}\n'
        if 'ac:height' in image_attrs:
            height = image_attrs['ac:height']
            image_markup = image_markup + f'{" " * 3}   :height: {height}px\n'
        return image_markup

    def _print_navigable_strs(self, tag):
        for child in tag.children:
            if isinstance(child, NavigableString):
                # pdb.set_trace()
                self._lines(child.string)

    def _check_parent_code_block(self, tag: Tag):
        if tag.parent and tag.parent.parent:
            if tag.parent.name == "ac:rich-text-body" or tag.parent.parent.name == "ac:rich-text-body":
                return True
        return False

    def _is_parent_a_macro_or_rich_text(self, tag: Tag) -> bool:
        if tag.parent:
            if tag.parent.name == "ac:rich-text-body" or tag.parent.name == "ac:structured-macro":
                return True

            elif tag.parent.parent:                
                if tag.parent.parent.name == "ac:rich-text-body" or tag.parent.parent.name == "ac:structured-macro":
                    return True
        return False

    def _is_dupicate(self, some_str: str)  -> bool:
        hash = hashlib.md5(some_str.encode('utf-8')).hexdigest()
        return hash in self._hash_dict
    
    def _create_heading_markup(self, tag: Tag):
        if tag and tag.string:
            my_string = tag.string.strip()
            if tag.name == "h1":
                the_string = "\n" + my_string + "\n" + "-" * len(my_string) + "\n\n"
                self._add_string(the_string)
            elif tag.name == "h2":
                the_string = "\n" + my_string + "\n" + "^" * len(my_string) + "\n\n"
                self._add_string(the_string)
            elif tag.name == "h3":
                the_string = "\n" + my_string + "\n" + ":" * len(my_string) + "\n\n"
                self._add_string(the_string)
            elif tag.name == "h4":
                the_string = "\n" + my_string + "\n" + ";" * len(my_string) + "\n\n"
                self._add_string(the_string)

    def _create_code_block(self, tag: Tag):
        if tag and tag.string:
            my_string = tag.string.strip()
            if len(my_string) > 0:
                # my_string = my_string.replace(".", ".\n")
                the_string = f"::\n\n   {my_string}\n\n"
                self._add_string(the_string)

    def _create_structured_macro_markup(self, tag: Tag):
        if tag:
            if tag.attrs and tag.attrs['ac:name'] == "note":
                self._create_code_block(tag)
            elif tag.attrs and tag.attrs['ac:name'] == "code":
                tag = tag.find_next("ac:plain-text-body")
                self._create_code_block(tag)
            elif tag.attrs and tag.attrs['ac:name'] == "anchor":
                anchor_id = str(uuid4())[0:8]
                self._link_cache[tag.string.strip()] = anchor_id
                self._lines.append(f".. _{anchor_id}:\n")
            elif self._has_rich_text_body_tag(tag):
                self._create_code_block(tag)

    def _create_structured_macro_markupv2(self, tag: Tag) -> CodeBlock:
        if tag:
            if tag.attrs and tag.attrs['ac:name'] == "note":
                return self._rst_converter.create_code_block(get_tag_text(tag))
            elif tag.attrs and tag.attrs['ac:name'] == "code":
                tag = tag.find_next("ac:plain-text-body")
                return self._rst_converter.create_code_block(get_tag_text(tag))
            elif tag.attrs and tag.attrs['ac:name'] == "anchor":
                pass
                # anchor_id = str(uuid4())[0:8]
                # self._link_cache[tag.string.strip()] = anchor_id
                # self._lines.append(f".. _{anchor_id}:\n")
            elif self._has_rich_text_body_tag(tag):
                return self._rst_converter.create_code_block(get_tag_text(tag))

    def _create_link_markup(self, tag: Tag):
        if tag:
            if "ac:anchor" in tag.attrs:
                title = tag.attrs['ac:anchor']
                anchor_label = self._link_cache[title]
                self._lines.append(f":ref:`{title} <{anchor_label}>`")

    def _create_paragraph_markup(self, tag: Tag):
        if tag and tag.string:
            if self._is_parent_a_macro_or_rich_text(tag):
                pass            
            elif tag.name == "strong":
                my_string = tag.string.strip()
                if len(my_string) > 0:
                    my_string = my_string.replace(".", ".\n")
                    self._add_string(f"**{my_string}**\n")
            elif tag.name == "p":
                my_string = tag.string.strip()
                if len(my_string) > 0:
                    my_string = my_string.replace(".", ".\n")
                    self._add_string(f"{my_string}\n")

    def _handle_nested_text(self, tag: Tag, the_string: str="") -> str:
        if tag:
            if isinstance(tag, NavigableString):
                if tag and tag.string:
                    the_string += tag.string.strip()
            elif isinstance(tag, Tag):
                if (tag.name == "p" or tag.name == "a" or tag.name == "span" or tag.name == "strong") and tag.string:
                    the_string += tag.string.strip()
                if tag.name == "ol" or tag.name == "ul" or tag.name == "li":
                    return the_string
            if self._has_children(tag):
                for child in tag.children:
                    the_string += self._handle_nested_text(child, the_string)
        return the_string

    def _create_list_data_struct(self, tag: Tag) -> List:
        list_items = tag.find_all("li", recursive=False)
        list_data_struct = []
        for list_item in list_items:
            text = get_tag_text(list_item, "ol", "ul", "ac:structured-macro")
            if text != None:
                list_data_struct.append(text)

            if self._has_children(list_item):
                for child in list_item.children:
                    if self._is_structured_macro_tag(child):
                        list_data_struct.append(self._create_structured_macro_markupv2(child))
                    if self._is_image_tag(child):
                        list_data_struct.append(self._create_image_markup(child))

            if self._has_tag(list_item, "ol"):
                list_data_struct.append(self._create_list_data_struct(list_item.find_next("ol")))
            elif self._has_tag(list_item, "ul"):
                list_data_struct.append(self._create_list_data_struct(list_item.find_next("ul")))
            
        return list_data_struct

    def _create_table_markup(self, tag: Tag):
        if tag.name == "table":
            grid = []
            for row in tag.find_all("tr"):
                if self._has_children(row):
                    row_list = []
                    for child in row.children:
                        if child.name == "th" or child.name == "td":
                            if child and child.text:
                                row_list.append(child.text.strip())
                    grid.append(row_list)

            self._lines.append(make_table(grid) + "\n")

    def _process_tag(self, tag: Tag, indent=0):
        print_tag(tag)
        processed = False
        if self._is_heading_tag(tag):
            self._create_heading_markup(tag)
        elif self._is_paragraph_tag(tag) or self._is_span_tag(tag) or self._is_strong_tag(tag):
            self._create_paragraph_markup(tag)
        elif self._is_structured_macro_tag(tag):
            self._create_structured_macro_markup(tag)
        elif self._is_break_tag(tag):
            self._lines.append("\n")
        elif self._is_image_tag(tag):
            self._lines.append(self._create_image_markup(tag))
        elif self._is_ordered_list_tag(tag) or self._is_unordered_list_tag(tag):
            list_data_struct = self._create_list_data_struct(tag)
            self._lines.append(self._rst_converter.create_list(list_data_struct))
            processed = True
        elif self._is_table_tag(tag):
            self._create_table_markup(tag)
            processed = True
        elif self._is_link_tag(tag):
            self._create_link_markup(tag)
            
        elif isinstance(tag, NavigableString):
            if tag and tag.string:
                self._lines.append(tag.string + "\n")
        
        if self._has_children(tag) and not processed:
            # print("Processing children")
            for child in tag.children:
                self._process_tag(child)

    def transform(self):
        self._create_top_level_heading(self._page_title)
        for tag in self._soup.find_all(recursive=False): #type: Tag
            self._process_tag(tag)
            self._lines.append("\n")
            with open("sphinx/pages/mytest.rst", "w") as f:
                f.writelines(self._lines)


def main():
    transformer = ConfluenceTransformer(CONFLUENCE_SAMPLE)
    transformer.transform()
    

if __name__ == '__main__':
    main()