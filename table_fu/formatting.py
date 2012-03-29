"""
Utilities to format values into more meaningful strings.
Inspired by James Bennett's template_utils and Django's
template filters.
"""
import re
import statestyle


def ap_state(value):
    """
    Converts a state's name, postal abbreviation or FIPS to A.P. style.
    
    Example usage:
    
        >> ap_state("California")
        'Calif.'
    
    """
    try:
        return statestyle.get(value).ap
    except:
        return value


def capfirst(value, failure_string='N/A'):
    """
    Capitalizes the first character of the value.
    
    If the submitted value isn't a string, returns the `failure_string` keyword
    argument.
    
    Cribbs from django's default filter set
    """
    try:
        value = value.lower()
        return value[0].upper() + value[1:]
    except:
        return failure_string


def dollars(value):
    return u'$%s'% intcomma(value)


def dollar_signs(value, failure_string='N/A'):
    """
    Converts an integer into the corresponding number of dollar sign symbols.
    
    If the submitted value isn't a string, returns the `failure_string` keyword
    argument.
    
    Meant to emulate the illustration of price range on Yelp.
    """
    try:
        count = int(value)
    except ValueError:
        return failure_string
    string = ''
    for i in range(0, count):
        string += '$'
    return string


def image(value, width='', height=''):
    """
    Accepts a URL and returns an HTML image tag ready to be displayed.
    
    Optionally, you can set the height and width with keyword arguments.
    """
    style = ""
    if width:
        style += "width:%s" % width
    if height:
        style += "height:%s" % height
    data_dict = dict(src=value, style=style)
    return '<img src="%(src)s" style="%(style)s">' % data_dict


def link(title, url):
    return u'<a href="%(url)s" title="%(title)s">%(title)s</a>' % {
        'url': url,
        'title': title
    }


def intcomma(value):
    """
    Borrowed from django.contrib.humanize
    
    Converts an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    orig = str(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new)


def stateface(value):
    """
    Converts a state's name, postal abbreviation or FIPS to ProPublica's stateface
    font code.
    
    Example usage:
    
        >> stateface("California")
        'E'
    
    Documentation: http://propublica.github.com/stateface/
    """
    try:
        return statestyle.get(value).stateface
    except:
        return value


def state_postal(value):
    """
    Converts a state's name, or FIPS to its postal abbreviation
    
    Example usage:
    
        >> ap_state("California")
        'Calif.'
    
    """
    try:
        return statestyle.get(value).postal
    except:
        return value


DEFAULT_FORMATTERS = {
    'ap_state': ap_state,
    'capfirst': capfirst,
    'dollars': dollars,
    'dollar_signs': dollar_signs,
    'intcomma': intcomma,
    'image': image,
    'link': link,
    'stateface': stateface,
    'state_postal': state_postal,
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
    '$1,200'
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
