"""
Utilities to format values into more meaningful strings.
Inspired by James Bennett's template_utils and Django's
template filters.
"""

def link(title, url):
    return u'<a href="%(url)s" title="%(title)s">%(title)s</a>' % {'url': url, 'title': title}


DEFAULT_FORMATTERS = {
    'link': link
}

class Formatter(object):
    """
    A formatter is a function (or any callable, really)
    that takes a value and returns a nicer-looking value,
    most likely a sting.
    
    Formatter stores and calls those functions, keeping
    the namespace uncluttered.
    
    Formatting functions should take a value as the first
    argument--usually the value of the Datum on which the
    function is called--followed by any number of positional
    arguments.
    
    In the context of TableFu, those arguments may refer to
    other columns in the same row.
    
    >>> formatter = Formatter()
    >>> formatter(1200, 'intcomma')
    '1,200'
    >>> formatter(1200, 'dollars')
    '$1200.00'
    """
    
    def __init__(self):
        self._filters = {}
        for name, func in DEFAULT_FORMATTERS.items():
            self.register(name, func)
    
    def __call__(self, value, func, *args):
        if not callable(func):
            func = self._filters[func]
        
        return func(value, *args)
    
    def register(self, name=None, func=None):
        if not func and not name:
            return

        if callable(name) and not func:
            func = name
            name = func.__name__
        elif func and not name:
            name = func.__name__
        
        self._filters[name] = func
    
    def unregister(self, name=None, func=None):
        if not func and not name:
            return
        if not name:
            name = func.__name__
        
        if name not in self._filters:
            return
        
        del self._filters[name]
        

# Unless you need to subclass or keep formatting functions
# isolated, you can just import this instance.
format = Formatter()
