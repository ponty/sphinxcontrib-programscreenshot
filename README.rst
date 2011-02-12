This Sphinx_ 1.0 extension executes programs during the build step and
includes their screenshot into the documentation.
GUI version of the :py:mod:`sphinxcontrib.programoutput` extension.


home: https://github.com/ponty/sphinxcontrib-programscreenshot

documentation: http://ponty.github.com/sphinxcontrib-programscreenshot


Basic usage
============
::

    .. program-screenshot:: xmessage hello
        :prompt:

How it works
========================

#. start Xvfb headless X server using PyVirtualDisplay_
#. redirect program display to Xvfb server by setting $DISPLAY variable.
#. wait some seconds
#. take screenshot by pyscreenshot_ which needs scrot.
#. use ``.. image::`` directive to display image



Installation
============

General
--------

 * install Xvfb_ and Xephyr_
 * install PIL_
 * install scrot
 * install setuptools_ or pip_
 * install the program:

if you have setuptools_ installed::

    # as root
    easy_install sphinxcontrib-programscreenshot

if you have pip_ installed::

    # as root
    pip install sphinxcontrib-programscreenshot

Ubuntu
----------
::

    sudo apt-get install python-setuptools
    sudo apt-get install scrot
    sudo apt-get install xvfb
    sudo apt-get install xserver-xephyr
    sudo apt-get install python-imaging
    sudo easy_install sphinxcontrib-programscreenshot


Uninstall
----------
::

    # as root
    pip uninstall sphinxcontrib-programscreenshot


.. _Sphinx: http://sphinx.pocoo.org/latest
.. _`sphinxcontrib-ansi`: http://packages.python.org/sphinxcontrib-ansi
.. _`sphinx-contrib`: http://bitbucket.org/birkenfeld/sphinx-contrib
.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _Xvfb: http://en.wikipedia.org/wiki/Xvfb
.. _Xephyr: http://en.wikipedia.org/wiki/Xephyr
.. _PIL: http://www.pythonware.com/library/pil/
.. _pyscreenshot: https://github.com/ponty/pyscreenshot
.. _PyVirtualDisplay: https://github.com/ponty/PyVirtualDisplay


