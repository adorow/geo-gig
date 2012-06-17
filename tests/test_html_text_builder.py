
import html_text_builder

import unittest

class TestHtmlTextBuilder(unittest.TestCase):
    "Test the class HtmlTextBuilder."
    
    def test_appending_text(self):
        # test the text appending function in the HtmlTextBuilder class.
        builder = html_text_builder.HtmlTextBuilder()
        self.assertEquals('', builder.get_text())
        self.assertEquals('', str(builder))
        text_to_add = 'new text added'
        builder.text(text_to_add)
        self.assertEquals(text_to_add, builder.get_text())
        self.assertEquals(text_to_add, str(builder))
        text_to_add2 = 'another text added'
        builder.text(text_to_add2)
        self.assertEquals(text_to_add + text_to_add2, builder.get_text())
        self.assertEquals(text_to_add + text_to_add2, str(builder))
        
    def test_appending_linebreak(self):
        # test the linebreak appending function
        builder = html_text_builder.HtmlTextBuilder()
        self.assertEquals('', builder.get_text())
        self.assertEquals('', str(builder))
        
        br = '<br />'
        
        builder.linebreak()
        self.assertEquals(br, builder.get_text())
        self.assertEquals(br, str(builder))
        
        builder = html_text_builder.HtmlTextBuilder()
        n = 5
        builder.linebreak(n)
        self.assertEquals(br * n, builder.get_text())
        self.assertEquals(br * n, str(builder))
        