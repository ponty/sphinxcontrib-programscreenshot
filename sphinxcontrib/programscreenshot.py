# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst.directives import flag, unchanged
from easyprocess import EasyProcess
from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import SmartDisplay, DisplayTimeoutError
import Image
import ImageChops
import docutils.parsers.rst.directives.images
import logging
import path
import pyscreenshot
import time

"""
    sphinxcontrib.programscreenshot
    ================================

    This extension provides a directive to include the screenshot of commands as
    image while building the docs.

"""

__version__ = '0.0.2'
   
log = logging.getLogger(__name__)
log.debug('sphinxcontrib.programscreenshot (version:%s)' % __version__)

def autocrop(im, bgcolor):
    '''Crop borders off an image.

     @param im Source image.
     @param bgcolor Background color, using either a color tuple or
     a color name (1.1.4 only).
     @return An image without borders, or None if there's no actual
     content in the image.
    '''
    if im.mode != "RGB":
        im = im.convert("RGB")
    bg = Image.new("RGB", im.size, bgcolor)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return None # no contents

class ProgramScreenshotError(Exception):
    pass

def prog_shot(cmd, f, wait, timeout, screen_size, visible, bgcolor):
    '''start process in headless X and create screenshot after 'wait' sec.
    Repeats screenshot until it is not empty if 'repeat_if_empty'=True.

    wait: wait at least N seconds after first window is displayed,
    it can be used to skip splash screen 

    :param enable_crop: True -> crop screenshot 
    :param wait: int 
    '''
    disp = SmartDisplay(visible=visible, size=screen_size, bgcolor=bgcolor)
    proc = EasyProcess(cmd)
    
    def func():
        try:
            img = disp.waitgrab(timeout=timeout)
        except DisplayTimeoutError as e:
            raise DisplayTimeoutError(str(e) + ' ' + str(proc))
        if wait:
            proc.sleep(wait)
            img = disp.grab()
        return img
    
    img = disp.wrap(proc.wrap(func))()
    if img:
        img.save(f)
    return (proc.stdout, proc.stderr)


parent = docutils.parsers.rst.directives.images.Image
images_to_delete = []
image_id = 0
class ProgramScreenshotDirective(parent):
    option_spec = parent.option_spec.copy()
    option_spec.update(dict(
                       prompt=flag,
                       screen=unchanged,
                       wait=unchanged,
                       stdout=flag,
                       stderr=flag,
                       visible=flag,
                       timeout=unchanged,
                       bgcolor=unchanged,
                       ))
    def run(self):
        screen = '1024x768' #default
        if 'screen' in self.options:
            screen = self.options['screen']
        screen = tuple(map(int, screen.split('x')))

        wait = 0 #default
        if 'wait' in self.options:
            wait = self.options['wait']
        wait = float(wait)
        
        timeout = 12    #default
        if 'timeout' in self.options:
            timeout = self.options['timeout']
        timeout = float(timeout)
        
        bgcolor = 'white'    
        if 'bgcolor' in self.options:
            bgcolor = self.options['bgcolor']
        
        visible = 'visible' in self.options
        
        cmd = str(self.arguments[0])
        
        #d=path.path('shots')
        #if not d.exists():
        #    d.makedirs()
        global image_id
        #f = 'screenshot_%s_id%s.png' % (time.ctime().replace(' ', '_'), str(image_id))
        f = 'screenshot_id%s.png' % (str(image_id))
        image_id += 1
        fabs = path.path(self.src).dirname() / (f)
        images_to_delete.append(fabs)

        o = prog_shot(cmd, fabs, screen_size=screen, wait=wait, timeout=timeout, visible=visible, bgcolor=bgcolor)

        self.arguments[0] = f
        x = parent.run(self)

        output = ''
        if 'stdout' in self.options:
            output += o[0] 
            if o[0]:
                output += '\n'

        if 'stderr' in self.options:
            output += o[1]
            if o[1]:
                output += '\n'

        if 'prompt' in self.options:
            # TODO:
            #if app.config.programoutput_use_ansi:
            #    # enable ANSI support, if requested by config
            #    from sphinxcontrib.ansi import ansi_literal_block
            #    node_class = ansi_literal_block
            #else:
            #    node_class = nodes.literal_block

            # TODO: get app
            #tmpl = app.config.programoutput_prompt_template
            tmpl = '$ %(command)s\n%(output)s'
            output = tmpl % dict(command=cmd, output=output)

        node_class = nodes.literal_block
        if output:
            x = [node_class(output, output)] + x

        return x

def cleanup(app, exception):
    for x in images_to_delete:
        f = path.path(x)
        if f.exists():
            log.debug('removing image:' + x)
            f.remove()

def setup(app):
    #app.add_config_value('programoutput_use_ansi', False, 'env')
    #app.add_config_value('programscreenshot_prompt_template',
    #                     '$ %(command)s\n%(output)s', 'env')
    app.add_directive('program-screenshot', ProgramScreenshotDirective)
    app.connect('build-finished', cleanup)

#logging.basicConfig(level=logging.DEBUG)
