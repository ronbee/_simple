"""press - a KISS reporting tool."""

__version__ = '0.0.1'
__author__ = 'info@4t2.pw'
__all__ = []

import pkg_resources
import markdown
from jinja2 import Template
from matplotlib import figure

from bokeh import plotting as bokeh_plotting
from bokeh.models import layouts as bokeh_layouts
from bokeh import __version__ as bokeh_ver

from os import environ

if 'BACKEND' in environ:
    from matplotlib import pyplot
    pyplot.switch_backend('agg')

_md_ = markdown.Markdown()

_aux_func_registry_ = []


def _content_handler_(type_def):
    def content_handler_wrap(func):
        _aux_func_registry_.append((func, type_def))
        return func

    return content_handler_wrap


@_content_handler_((str, bytes))
def _handle_md(md_text):
    from html.parser import HTMLParser

    class AuxHTMLParser(HTMLParser):
        a = []

        def handle_starttag(self, tag, attrs):
            self.a.append("s")

        def handle_endtag(self, tag):
            self.a.append("e")

    parser = AuxHTMLParser()
    parser.feed(md_text)

    return md_text if 's' in parser.a and 'e' in parser.a else _md_.convert(md_text)


@_content_handler_((figure.Figure,))
def convert_fig_to_html(fig):
    """ Convert Matplotlib figure 'fig' into a <img> tag for HTML use using base64 encoding. """
    import urllib
    import io, base64

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read())

    return '<img src="data:image/png;base64,{}">'.format(urllib.parse.quote(data))


@_content_handler_((bokeh_plotting.Figure, bokeh_layouts.Column, bokeh_layouts.Row))
def convert_bokeh_fig_to_html(fig):
    from bokeh.embed import components

    script, div = components(fig)

    return '%s %s' % (div, script)


def html_it(item):
    for f, tdef in _aux_func_registry_:
        if isinstance(item, tdef):
            return f(item)
    return None  # i.e., didn't find


_BOKEH_HEAD_LINKS_ = """
    <!-- BOKEH -->
    <link href="http://cdn.pydata.org/bokeh/release/bokeh-%s.min.css" rel="stylesheet" type="text/css">
    <link href="http://cdn.pydata.org/bokeh/release/bokeh-widgets-%s.min.css" rel="stylesheet" type="text/css">
    <link href="http://cdn.pydata.org/bokeh/release/bokeh-tables-%s.min.css" rel="stylesheet" type="text/css">
    <script src=\"http://cdn.pydata.org/bokeh/release/bokeh-%s.min.js\"></script>
    <script src=\"http://cdn.pydata.org/bokeh/release/bokeh-widgets-%s.min.js\"></script>
    <script src=\"http://cdn.pydata.org/bokeh/release/bokeh-tables-%s.min.js\"></script>
    
    """ % ((bokeh_ver,)*6)


class Report(object):
    def __init__(self, title='A Press Report', subtitle='', headlinks=''):
        self.head_links = _BOKEH_HEAD_LINKS_ + headlinks
        self.title = title
        self.subtitle = subtitle
        self._report = []

    def attach(self, item):
        html_str = html_it(item)
        self._report.append(html_str)
        return 'ok' if html_str else ('does not have an attach function for type: %s' % type(item))

    def html(self):
        template = Template("".join( chr(x) for x in
                                    pkg_resources.resource_string(__name__,
                                                                  "templates/report0.html")))
        return template.render(dict(title=self.title, subtitle=self.subtitle,
                                    htmlbody='\n'.join(self._report), head_links=self.head_links))

    def show(self, html_file_name=None):
        import webbrowser, os, uuid, re
        saved_html_file_name = html_file_name if html_file_name else 'press_%s_%s.html' % (re.sub('\s',
                                                                                                    '_',
                                                                                                    self.title),
                                                                                                 uuid.uuid4())
        with open(saved_html_file_name, 'w') as fout:
            fout.write(self.html())

        webbrowser.open('file://' + os.path.realpath(saved_html_file_name))







