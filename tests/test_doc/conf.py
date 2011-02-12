# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)

import sys, os

from path import path
sys.path.insert(0, path('..').abspath())

needs_sphinx = '1.0'

extensions = [
            #'sphinx.ext.intersphinx',
              'sphinxcontrib.programscreenshot',
              ]

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib-programoutput'
copyright = u'2011, ponty'
version = '0.1.0'
#release =

exclude_patterns = ['_build/*']

html_theme = 'default'
html_static_path = []

#intersphinx_mapping = {
#    'ansi': ('http://packages.python.org/sphinxcontrib-ansi', None)}


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')
