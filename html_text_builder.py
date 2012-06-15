
class HtmlTextBuilder:
    "Builder to create HTML texts used in the geo-gig pages."
    def __init__(self):
        "Creates a new HTtmlTextBuilder."
        self._text = ''

    def get_text(self):
        "Gets the built text."
        return self._text
        
    def text(self, text):
        "Appends new text to the builder."
        return self._append(text)
    
    def linebreak(self, n=1):
        "Appends line breaks to the builder. If 'n' is ommited, only one line break is added." 
        return self._append('<br />' * n)
    
    def _append(self, text):
        self._text += text
        return self
        
    def __str__(self):
        return self.get_text()