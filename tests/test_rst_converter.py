import os
import pytest
import pdb

from pytest import MonkeyPatch
from pathlib import Path
from bs4 import BeautifulSoup
from confluence_converter.rst_converter import RSTConverter, indent_content
from confluence_converter.exporter import MyConfluenceExporter


TESTFILES_DIR = os.path.dirname(os.path.realpath(__file__)) + "/testfiles"

@pytest.fixture
def mock_download_image(monkeypatch: MonkeyPatch):

    def mock_download_image(self, filename, page):
        return None
        
    monkeypatch.setattr(MyConfluenceExporter, "download_image", mock_download_image)

# class TestComplex:

#     def test_image_codeblock_imbedded(self, mock_download_image):
#         c = RSTConverter(is_confluence_mock=True)
#         test = """<ol><li><ac:structured-macro ac:macro-id="9ff3e27d-c485-4496-9c63-812e316fb85d" ac:name="code" ac:schema-version="1"><ac:parameter ac:name="language">bash</ac:parameter><ac:plain-text-body><![CDATA[def transform(self):
#     self._create_top_level_heading(self._page_title)
#     for tag in self._soup.find_all(recursive=False): #type: Tag
#         self._process_tag(tag)
#         self._lines.append("\n")
#         with open("sphinx/pages/mytest.rst", "w") as f:
#             f.writelines(self._lines)]]></ac:plain-text-body></ac:structured-macro></li></ol>
# """
#         soup = BeautifulSoup(test)
#         value = c.create_list_markup(soup.find("ol"))
#         pdb.set_trace()
#         assert "" == value

#         content = Path(TESTFILES_DIR + "/image_codeblock_imbedded_in_list.html").read_text()
#         soup = BeautifulSoup(content)                
#         value = c.create_list_markup(soup.find("ol"))
#         assert "" == value


class TestRSTConverter:

    def test_create_code_block_markup(self):
        c = RSTConverter(is_confluence_mock=True)

        soup = BeautifulSoup('<li></li>')

        soup = BeautifulSoup('<ac:structured-macro ac:name="info"><ac:rich-text-body><p><strong>Foo bar.  Foo bar2.Foo bar3 </strong></p></ac:rich-text-body></ac:structured-macro>')
        value = c.create_code_block_markup(soup.find("ac:structured-macro"))
        assert '\n\n::\n\n   Foo bar.  Foo bar2.Foo bar3.\n\n' == value

        soup = BeautifulSoup('<ac:structured-macro><ac:rich-text-body>Foo bar.  Foo bar2.Foo bar3 </ac:rich-text-body></ac:structured-macro>')
        value = c.create_code_block_markup(soup.find("ac:structured-macro"))
        assert '\n\n::\n\n   Foo bar.  Foo bar2.Foo bar3.\n\n' == value

        soup = BeautifulSoup('<ac:structured-macro><ac:rich-text-body></ac:rich-text-body></ac:structured-macro>')
        value = c.create_code_block_markup(soup.find("ac:structured-macro"))
        assert '' == value

        code_block = """<ac:structured-macro ac:macro-id="9ff3e27d-c485-4496-9c63-812e316fb85d" ac:name="code" ac:schema-version="1"><ac:parameter ac:name="language">bash</ac:parameter><ac:plain-text-body><![CDATA[def transform(self):
    self._create_top_level_heading(self._page_title)
    for tag in self._soup.find_all(recursive=False): #type: Tag
        self._process_tag(tag)
        self._lines.append("\n")
        with open("sphinx/pages/mytest.rst", "w") as f:
            f.writelines(self._lines)]]></ac:plain-text-body></ac:structured-macro>
"""
        soup = BeautifulSoup(code_block)
        value = c.create_code_block_markup(soup.find("ac:structured-macro"))
        assert '\n\n::\n\n   def transform(self):\n       self._create_top_level_heading(self._page_title)\n       for tag in self._soup.find_all(recursive=False): #type: Tag\n           self._process_tag(tag)\n           self._lines.append("\n   ")\n           with open("sphinx/pages/mytest.rst", "w") as f:\n               f.writelines(self._lines)\n\n' == value

        with pytest.raises(TypeError):
            soup = BeautifulSoup('<ac:structured-macro ac:name="blah"><p><strong>Foo bar.  Foo bar2.Foo bar3 </strong></p></ac:structured-macro>')
            c.create_code_block_markup(soup.find("ac:structured-macro"))

        with pytest.raises(TypeError):
            soup = BeautifulSoup('<p><strong>Foo bar.  Foo bar2.Foo bar3 </strong></p>')
            c.create_code_block_markup(soup.find("ac:structured-macro"))

        with pytest.raises(TypeError):            
            c.create_code_block_markup(None)

        with pytest.raises(TypeError):
            soup = BeautifulSoup('<strong>Foo bar.  Foo bar2.Foo bar3 </strong>')
            c.create_code_block_markup(soup.find("ac:structured-macro"))


    def test_create_image_markup(self):
        c = RSTConverter(is_confluence_mock=True)
        soup = BeautifulSoup('<ac:image ac:height="202" ac:thumbnail="true"><ri:attachment ri:filename="CVAH Shields.jpg"></ri:attachment></ac:image><br/>')
        markup, filename = c.create_image_markup(soup.find("ac:image"))

        assert "\n\n   .. figure:: /images/CVAH\\ Shields.jpg\n      :height: 202px\n\n" == markup
        assert "CVAH\\ Shields.jpg" == filename        

        with pytest.raises(TypeError):
            soup = BeautifulSoup('<p>invalid<p>')
            c.create_image_markup(soup.find("p"))

        with pytest.raises(TypeError):            
            c.create_image_markup(None)

    def test_indent(self):
        my_string = "2. sub item 2\n\n   .. figure:: /images/add_installer_config.jpg\n      :height: 250px\n"
        value = indent_content(my_string, 1)
        assert '   2. sub item 2\n\n      .. figure:: /images/add_installer_config.jpg\n         :height: 250px\n' == value
        value = indent_content("blah", 0)
        assert "blah" == value
        value = indent_content(None, 0)
        assert "" == value
        value = indent_content("", 0)
        assert "" == value

    def test_create_list_markup(self, mock_download_image):
        c = RSTConverter(is_confluence_mock=True)
        soup = BeautifulSoup("<ol><li>Item 1<ol><li>sub item 1</li><li>sub item 2</li></ol></li><li>Item 2<ol><li>sub2 item 1</li><li>sub2 item 2</li></ol></li></ol>", "html.parser")        
        value = c.create_list_markup(soup.find("ol"))
        assert "\n1. Item 1\n\n   1. sub item 1\n   2. sub item 2\n2. Item 2\n\n   1. sub2 item 1\n   2. sub2 item 2\n" == value

        soup = BeautifulSoup("<ol><li><p>Item 1 <strong>blah</strong></p><ol><li>sub item 1</li><li>sub item 2</li></ol></li><li>Item 2<ol><li>sub2 item 1</li><li>sub2 item 2</li></ol></li></ol>", "html.parser")        
        value = c.create_list_markup(soup.find("ol"))
        assert '\n1. Item 1 **blah**\n\n   1. sub item 1\n   2. sub item 2\n2. Item 2\n\n   1. sub2 item 1\n   2. sub2 item 2\n' == value

        soup = BeautifulSoup("<ol><li><p>Item 1 <strong>blah</strong></p><ol><li><p>sub item 1 <em>blah2</em></p></li><li>sub item 2</li></ol></li><li>Item 2<ol><li>sub2 item 1</li><li>sub2 item 2</li></ol></li></ol>", "html.parser")        
        value = c.create_list_markup(soup.find("ol"))
        assert '\n1. Item 1 **blah**\n\n   1. sub item 1 *blah2*\n   2. sub item 2\n2. Item 2\n\n   1. sub2 item 1\n   2. sub2 item 2\n' == value
        
        soup = BeautifulSoup('<ol><li><p>This is a test<ac:image ac:alt="Blah" ac:height="250" ac:queryparams="effects=border-simple,blur-border" ac:title="Blah"><ri:attachment ri:filename="add_installer_config.jpg"></ri:attachment></ac:image></p></li></ol>')
        value = c.create_list_markup(soup.find("ol"))
        assert '\n1. This is a test\n\n   .. figure:: /images/add_installer_config.jpg\n      :height: 250px\n' == value

        soup = BeautifulSoup('<ol><li>Item 1<ol><li>sub item 1</li><li><p>sub item 2<ac:image ac:alt="Blah" ac:height="250" ac:queryparams="effects=border-simple,blur-border" ac:title="Blah"><ri:attachment ri:filename="add_installer_config.jpg"></ri:attachment></ac:image></p></li></ol></li><li>Item 2<ol><li>sub2 item 1</li><li>sub2 item 2</li></ol></li></ol>')
        value = c.create_list_markup(soup.find("ol"))
        assert '\n1. Item 1\n\n   1. sub item 1\n   2. sub item 2\n\n      .. figure:: /images/add_installer_config.jpg\n         :height: 250px\n2. Item 2\n\n   1. sub2 item 1\n   2. sub2 item 2\n' == value

        soup = BeautifulSoup('<ol><li><span class="NormalTextRun SCXW118477166 BCX0">Log in to the </span><span class="TextRun SCXW118477166 BCX0"><span class="NormalTextRun SCXW118477166 BCX0">ServiceNow portal (<a class="external-link" href="https://afdco.servicenowservices.com/sp" rel="nofollow">https://afdco.servicenowservices.com/sp</a></span></span><span class="TextRun SCXW118477166 BCX0">) i</span>f the installation fails:      <ol><li>Take note of the specific point in the installation at which the failure occurred</li><li>Which component was being installed?  </li><li>Which task was Ansible performing?</li><li>Check for error messages on the Portal page under the Notifications bell icon</li><li>Is there any useful information to be seen in the error messages?</li></ol></li></ol>')
        value = c.create_list_markup(soup.find("ol"))
        assert '\n1. Log in to the ) i f the installation fails:\n\n   1. Take note of the specific point in the installation at which the failure occurred\n   2. Which component was being installed?\n   3. Which task was Ansible performing?\n   4. Check for error messages on the Portal page under the Notifications bell icon\n   5. Is there any useful information to be seen in the error messages?\n' == value

        soup = BeautifulSoup('<ol><li>Type <strong>Snipping Tool </strong>in the Cortana search bar in the bottom left</li></ol>')
        value = c.create_list_markup(soup.find("ol"))
        assert '\n1. Type **Snipping Tool** in the Cortana search bar in the bottom left\n' == value

        # soup = BeautifulSoup('<ol><li><p>This is a test</p><p><ac:image ac:alt="Blah" ac:height="250" ac:queryparams="effects=border-simple,blur-border" ac:title="Blah"><ri:attachment ri:filename="add_installer_config.jpg"></ri:attachment></ac:image></p></li></ol>')        
        # value = c.create_list_markup(soup.find("ol"))
        # assert '\n1. This is a test\n\n   .. figure:: /images/add_installer_config.jpg\n      :height: 250px\n' == value

        with pytest.raises(TypeError):
            c.create_list_markup(None)            

        with pytest.raises(TypeError):
            soup = BeautifulSoup("<p>invalid<p>")
            c.create_list_markup(soup.find("p"))

    def test_create_link_markup(self):
        c = RSTConverter()
        soup = BeautifulSoup('<p><a href="https://www.google.com">https://www.google.com</a><p>', "html.parser")

        with pytest.raises(TypeError):
            c.create_link_markup(soup.find("p"))
        
        with pytest.raises(TypeError):
            c.create_link_markup(None)

        soup = BeautifulSoup('<a href="https://www.google.com">https://www.google.com</a> ', "html.parser")
        value = c.create_link_markup(soup.find("a"))
        assert "https://www.google.com" == value

        soup = BeautifulSoup('<a href="https://www.google.com"></a>', "html.parser")
        value = c.create_link_markup(soup.find("a"))
        assert "https://www.google.com" == value

        soup = BeautifulSoup('<a href="https://cnbc.com">Blah</a>', "html.parser")
        value = c.create_link_markup(soup.find("a"))
        assert "`Blah <https://cnbc.com>`_" == value
        
        soup = BeautifulSoup('<ac:link ac:anchor="Top Of Page"></ac:link>', "html.parser")
        value = c.create_link_markup(soup.find("ac:link"))
        assert "" == value

        soup = BeautifulSoup('<a href="https://confluence.di2e.net/pages/viewpage.action?pageId=275360146">Bug Reporting and System Change/Enhancement Requests</a>')
        value = c.create_link_markup(soup.find("a"))
        assert '`Bug Reporting and System Change/Enhancement Requests <https://confluence.di2e.net/pages/viewpage.action?pageId=275360146>`_' == value
        
        soup = BeautifulSoup('<ol><li>Refer to <a href="https://confluence.di2e.net/pages/viewpage.action?pageId=275360146">Bug Reporting and System Change/Enhancement Requests</a> to gain access and obtain User Guide</li></ol>')
        value = c.create_list_markup(soup.find("ol"))
        assert '\n1. Refer to `Bug Reporting and System Change/Enhancement Requests <https://confluence.di2e.net/pages/viewpage.action?pageId=275360146>`_ to gain access and obtain User Guide\n' == value

        c = RSTConverter(is_confluence_mock=True, link_cache={"Top Of Page": "somereference"})
        soup = BeautifulSoup('<ac:link ac:anchor="Top Of Page"></ac:link>', "html.parser")
        value = c.create_link_markup(soup.find("ac:link"))
        assert ":ref:`Top Of Page <somereference>`" == value
    
    def test_create_paragraph_markup(self, mock_download_image):
        c = RSTConverter(is_confluence_mock=True)
        soup = BeautifulSoup("<p>This is a paragraph <strong>I have bold text here. </strong>This is normal text again. <em> This is </em><em>Italicized text.  </em><u>This is underlined text.</u></p>", "html.parser")        
        value = c.create_paragraph_markup(soup.find("p"))
        assert 'This is a paragraph **I have bold text here.** This is normal text again. *This is* *Italicized text.* This is underlined text.\n'  == value

        soup = BeautifulSoup("<p>Test1</p>", "html.parser")        
        value = c.create_paragraph_markup(soup.find("p"))
        assert "Test1\n" == value

        soup = BeautifulSoup("<p><span>Test2</span></p>", "html.parser")
        value = c.create_paragraph_markup(soup.find("p"))
        assert "Test2\n" == value

        soup = BeautifulSoup("<strong>Test3</strong>", "html.parser")
        value = c.create_paragraph_markup(soup.find("strong"))
        assert "**Test3**\n" == value

        soup = BeautifulSoup("<strong></strong>", "html.parser")
        value = c.create_paragraph_markup(soup.find("strong"))
        assert "" == value

        soup = BeautifulSoup("<em></em>", "html.parser")
        value = c.create_paragraph_markup(soup.find("em"))
        assert "" == value

        soup = BeautifulSoup("<u></u>", "html.parser")
        value = c.create_paragraph_markup(soup.find("u"))
        assert "" == value

        soup = BeautifulSoup("<p>Test<strong>Test4</strong></p>", "html.parser")
        value = c.create_paragraph_markup(soup.find("p"))
        assert "Test **Test4**\n" == value

        soup = BeautifulSoup('<p style="text-align: center;"><ac:image ac:height="202" ac:thumbnail="true"><ri:attachment ri:filename="CVAH Shields.jpg"></ri:attachment></ac:image><br/><br/>HANDLING AND DESTRUCTION NOTICE<br/>- Handle in compliance with distribution statement and destroy by any method that will prevent disclosure of contents or reconstruction of the document.  <br/><br/></p>')
        value = c.create_paragraph_markup(soup.find("p"))
        assert '.. figure:: /images/CVAH\\ Shields.jpg\n      :height: 202px\n\n\n\nHANDLING AND DESTRUCTION NOTICE\n- Handle in compliance with distribution statement and destroy by any method that will prevent disclosure of contents or reconstruction of the document.\n\n\n' == value        

        soup = BeautifulSoup('<p><strong>Build the Communications Case:</strong><br/>Slot 1:  PDU<br/>Slot 2:  Switch (Dell 4112)<br/>Slot 3:  Server (Dell R440) <br/>Labeled: A<br/><br/><strong><ac:image ac:border="true" ac:height="189" ac:width="447"><ri:attachment ri:filename="worddav6c17d0845ed51f87688094e1d29defad.png"></ri:attachment></ac:image></strong><br/><strong>Face View of the Case with Slots Labeled<br/><br/></strong></p>')
        value = c.create_paragraph_markup(soup.find("p"))
        assert '**Build the Communications Case:**\nSlot 1:  PDU\nSlot 2:  Switch (Dell 4112)\nSlot 3:  Server (Dell R440)\nLabeled: A\n\n\n\n' == value
        
    def test_create_heading_markup(self):
        c = RSTConverter(is_confluence_mock=True)
        soup = BeautifulSoup("<h1>Test</h1>", "html.parser")
        value = c.create_heading_markup(soup.find("h1"))
        assert "\nTest\n----\n\n" == value

        soup = BeautifulSoup("<h2>Test</h2>", "html.parser")
        value = c.create_heading_markup(soup.find("h2"))
        assert "\nTest\n^^^^\n\n" == value

        soup = BeautifulSoup("<h3>Test</h3>", "html.parser")
        value = c.create_heading_markup(soup.find("h3"))
        assert "\nTest\n::::\n\n" == value

        soup = BeautifulSoup("<h4>Test</h4>", "html.parser")
        value = c.create_heading_markup(soup.find("h4"))
        assert "\nTest\n;;;;\n\n" == value

        soup = BeautifulSoup("<h4>   foo bar   </h4>", "html.parser")
        value = c.create_heading_markup(soup.find("h4"))
        assert "\nfoo bar\n;;;;;;;\n\n" == value
        
        soup = BeautifulSoup("<h2><span>foo bar <br/></span></h2>", "html.parser")
        value = c.create_heading_markup(soup.find("h2"))
        assert "\nfoo bar\n^^^^^^^\n\n" == value
                    
        with pytest.raises(TypeError):
            soup = BeautifulSoup("<p>Test</p>", "html.parser")
            c.create_heading_markup(soup.find("p"))
        
        soup = BeautifulSoup("<h4></h4>", "html.parser")
        value = c.create_heading_markup(soup.find("h4"))
        assert value == ''        

        with pytest.raises(TypeError):
            c.create_heading_markup(None)
