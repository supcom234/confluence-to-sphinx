from functools import reduce
from ossaudiodev import control_names
from typing import List, Union
from bs4.element import Tag



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


class RSTConverter:
    
    def create_list(self, content: List[Union[str, List, CodeBlock]], indent=0, output="") -> str:
        output += "\n"
        count = 1
        for item in content:
            if isinstance(item, list):                
                output = self.create_list(item, indent+1, output)
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

    def create_code_block(self, content: str) -> CodeBlock:
        if content != None and len(content) > 0:
            new_content = []
            for line in content.splitlines():
                new_content.append((" " * 3) + line)

            new_content = '\n'.join(new_content).rstrip()
            return CodeBlock(f"\n::\n\n{new_content}\n\n")

    def create_heading_markup(self, tag: Tag) -> str:
        if tag and len(tag.text) == 0:
            return ''

        if tag and tag.text:
            my_string = tag.text.strip()
            if len(my_string) == 0:
                return ''
            if tag.name == "h1":
                the_string = "\n" + my_string + "\n" + "-" * len(my_string) + "\n\n"
                return the_string
            elif tag.name == "h2":
                the_string = "\n" + my_string + "\n" + "^" * len(my_string) + "\n\n"
                return the_string
            elif tag.name == "h3":
                the_string = "\n" + my_string + "\n" + ":" * len(my_string) + "\n\n"
                return the_string
            elif tag.name == "h4":
                the_string = "\n" + my_string + "\n" + ";" * len(my_string) + "\n\n"
                return the_string

        raise ValueError("Invalid header tag: " + str(tag))

def main():
    c = RSTConverter()
    # s = ["Item one", "Item two", ["Subitem one", "Subitem two", ["subsub item one"] ]]
    # output = ""
    # print(c.create_list(s))
    t = 'def transform(self):\n    self._create_top_level_heading(self._page_title)\n    for tag in self._soup.find_all(recursive=False): #type: Tag\n        self._process_tag(tag)\n        self._lines.append("\\n")\n        with open("sphinx/pages/mytest.rst", "w") as f:\n            f.writelines(self._lines)'
    print(c.create_code_block(t))
    
    

if __name__ == '__main__':
    main()