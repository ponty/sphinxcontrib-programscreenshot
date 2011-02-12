# -*- coding: utf-8 -*-

import sys, os
import logging

from path import path
sys.path.insert(0, (path(__file__).dirname().dirname() ).abspath())
from sphinxcontrib.programscreenshot import __version__
release = __version__
#release = 'xxx'

project = u'sphinxcontrib-programscreenshot'
copyright = u'2011, ponty'
author='ponty'

logging.basicConfig(level=logging.DEBUG)

needs_sphinx = '1.0'

extensions = [
            #'sphinx.ext.intersphinx',
              'sphinxcontrib.programscreenshot',
             #'sphinx.ext.autodoc',
             #'sphinxcontrib.programoutput',
             #'sphinx.ext.graphviz',
             #'sphinx.ext.autosummary',
              ]
intersphinx_mapping = {'http://docs.python.org/': None}

source_suffix = '.rst'
master_doc = 'index'


exclude_patterns = ['_build/*']

html_theme = 'default'
html_static_path = []

#intersphinx_mapping = {
#    'ansi': ('http://packages.python.org/sphinxcontrib-ansi', None)}


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')
