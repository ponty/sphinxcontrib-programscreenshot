# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst.directives import flag, unchanged
from easyprocess import EasyProcess
from pyvirtualdisplay import Display
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

__version__ = '0.0.0'
   
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

def prog_shot(cmd, f, wait=1, timeout=60, screen_size=(1024, 768), repeat_if_empty=True, repeat_time=1, enable_crop=True, visible=False, bgcolor='white'):
    '''start process in headless X and create screenshot after 'wait' sec.
    Repeats screenshot until it is not empty if 'repeat_if_empty'=True.

    :param enable_crop: True -> crop screenshot '''
    disp = Display(visible=visible, size=screen_size, bgcolor=bgcolor).start()

    # display background color
    #imbg = Image.new('RGB', (1000,1000), bgcolor)
    #imbg.show()

    proc = EasyProcess(cmd).start()

    t = 0
    sleep_time = wait
    while 1:
        log.debug('sleeping %s secs' % str(sleep_time))
        time.sleep(sleep_time)
        t += sleep_time
        pyscreenshot.grab_to_file(f)
        im_in = Image.open(f)
        if enable_crop:
            im_out = autocrop(im_in, bgcolor=bgcolor)
        else:
            if im_in.getbbox():
                im_out = im_in
        if im_out:
            break
        path.path(f).remove()
        if not repeat_if_empty:
            break
        sleep_time = repeat_time
        if t > timeout:
            log.debug('timeout')
            disp.stop()
            assert 0, 'timeout cmd:"%s"' % cmd
            break

        log.debug('screenshot is empty, next try..')

    proc.stop()
    disp.stop()

    if im_out:
        im_out.save(f)
    else:
        log.debug('screenshot is empty!')
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
                       ))
    def run(self):
        screen = '1024x768'
        if 'screen' in self.options:
            screen = self.options['screen']
        screen = tuple(map(int, screen.split('x')))

        wait = 0.3
        if 'wait' in self.options:
            wait = self.options['wait']
            wait = float(wait)
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

        o = prog_shot(cmd, fabs, screen_size=screen, wait=wait, visible=visible)

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
