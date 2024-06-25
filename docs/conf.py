import pyvlq

project = pyvlq.__name__
author = "osoken"

version = pyvlq.__version__
release = pyvlq.__version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

language = "en"
