import pytest

from bs4 import BeautifulSoup
from confluence_converter.rst_converter import RSTConverter


class TestRSTConverter:
  
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
        

    def test_create_heading_markup_failures(self):
        c = RSTConverter()
        with pytest.raises(ValueError):
            soup = BeautifulSoup("<p>Test</p>", "html.parser")
            c.create_heading_markup(soup.find("p"))
        
        soup = BeautifulSoup("<h4></h4>", "html.parser")
        value = c.create_heading_markup(soup.find("h4"))
        assert value == ''        

        with pytest.raises(ValueError):
            c.create_heading_markup(None)

        