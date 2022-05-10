import pytest

from bs4 import BeautifulSoup
from confluence_converter.rst_converter import RSTConverter


class TestRSTConverter:
    #

    def test_create_image_markup(self):
        c = RSTConverter()
        soup = BeautifulSoup('<ac:image ac:height="202" ac:thumbnail="true"><ri:attachment ri:filename="CVAH Shields.jpg"></ri:attachment></ac:image><br/>')
        markup, filename = c.create_image_markup(soup.find("ac:image"))

        assert "\n   .. figure:: /images/CVAH\\ Shields.jpg\n      :height: 202px\n" == markup
        assert "CVAH\\ Shields.jpg" == filename

        with pytest.raises(TypeError):
            soup = BeautifulSoup('<p>invalid<p>')
            c.create_image_markup(soup.find("p"))

        with pytest.raises(TypeError):            
            c.create_image_markup(None)


    def test_create_list_markup(self):
        c = RSTConverter()
        soup = BeautifulSoup("<ol><li>Item 1<ol><li>sub item 1</li><li>sub item 2</li></ol></li><li>Item 2<ol><li>sub2 item 1</li><li>sub2 item 2</li></ol></li></ol>", "html.parser")
        value = c.create_list_markup(soup.find("ol"))
        assert "\n1. Item 1\n\n   1. sub item 1\n   2. sub item 2\n2. Item 2\n\n   1. sub2 item 1\n   2. sub2 item 2\n" == value

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
        
        c = RSTConverter(link_cache={"Top Of Page": "somereference"})
        soup = BeautifulSoup('<ac:link ac:anchor="Top Of Page"></ac:link>', "html.parser")
        value = c.create_link_markup(soup.find("ac:link"))
        assert ":ref:`Top Of Page <somereference>`" == value
    
    def test_create_paragraph_markup(self):
        c = RSTConverter()
        soup = BeautifulSoup("<p>This is a paragraph <strong>I have bold text here. </strong>This is normal text again. <em> This is </em><em>Italicized text.  </em><u>This is underlined text</u>.</p>", "html.parser")
        value = c.create_paragraph_markup(soup.find("p"))
        assert "This is a paragraph **I have bold text here.** *This is* *Italicized text.* This is underlined text\n" == value
        
        soup = BeautifulSoup("<p>Test1</p>", "html.parser")
        value = c.create_paragraph_markup(soup.find("p"))
        assert "Test1\n" == value

        soup = BeautifulSoup("<p><span>Test2</span></p>", "html.parser")
        value = c.create_paragraph_markup(soup.find("p"))
        assert "Test2\n" == value

        soup = BeautifulSoup("<strong>Test3</strong>", "html.parser")
        value = c.create_paragraph_markup(soup.find("strong"))
        assert "**Test3**\n" == value

        soup = BeautifulSoup("<p>Test<strong>Test4</strong></p>", "html.parser")
        value = c.create_paragraph_markup(soup.find("p"))
        assert "Test **Test4**\n" == value
        
    def test_create_heading_markup(self):
        c = RSTConverter()
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
