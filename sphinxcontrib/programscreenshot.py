from docutils import nodes
from docutils.parsers.rst import directives
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay, DisplayTimeoutError
import docutils.parsers.rst.directives.images
import logging
import path

"""
    sphinxcontrib.programscreenshot
    ================================

    This extension provides a directive to include the screenshot of commands as
    image while building the docs.

"""

__version__ = '0.0.4'
   
log = logging.getLogger(__name__)
log.debug('sphinxcontrib.programscreenshot (version:%s)' % __version__)

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
                       prompt=directives.flag,
                       screen=directives.unchanged,
                       wait=directives.nonnegative_int,
                       stdout=directives.flag,
                       stderr=directives.flag,
                       visible=directives.flag,
                       timeout=directives.nonnegative_int,
                       bgcolor=directives.unchanged,
                       ))
    def run(self):
        screen = self.options.get('screen', '1024x768')
        screen = tuple(map(int, screen.split('x')))
        wait = self.options.get('wait', 0)
        timeout = self.options.get('timeout', 12)
        bgcolor = self.options.get('bgcolor', 'white')
        visible = 'visible' in self.options
        cmd = str(self.arguments[0])
        
        global image_id
        f = 'screenshot_id%s.png' % (str(image_id))
        image_id += 1
        fabs = path.path(self.src).dirname() / (f)
        images_to_delete.append(fabs)

        o = prog_shot(cmd, fabs, screen_size=screen, wait=wait, 
                      timeout=timeout, visible=visible, bgcolor=bgcolor)

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

