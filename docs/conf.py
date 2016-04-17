#!/usr/bin/env python3
project = "Bars"
version = release = "0.0.1"
author = "Matt Riggott"
copyright = "2016 {}".format(author)


master_doc = "index"
source_suffix = ".rst"
language = None
today_fmt = "%d %B %Y"


exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
add_function_parentheses = True
todo_include_todos = False


html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_use_smartypants = True
html_domain_indices = False
html_use_index = False
html_show_sourcelink = False
html_show_sphinx = False
htmlhelp_basename = "Barsdoc"


extensions = [
    "sphinx.ext.intersphinx",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.4", None),
    "agate": ("http://agate.readthedocs.org/en/1.3.1/", None),
}
