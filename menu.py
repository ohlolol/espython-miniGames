## Pundo:
## implementation for the menu
## and gameloader
##
## Changes:
## 09.02.25: Creation

from ili9341 import Display, color565
from xpt2046 import Touch
from machine import Pin, SPI, PWM
from pndConfig import tasks as cfg # get Configuration
import sys # needed to load modules in runtime
import time
    
    
def color_rgb(r, g, b):
    return color565(r, g, b)


class TouchScreen(object):

    
    def __init__(self, rtCB): # pass callback to runtime and set as globals
        self.rtCB = rtCB
        self.mark_touch = True # True, False --> Show touch coordinates
        self.Touch_items = []
        self.Touch_callbacks = []
        
        self.spi_display = SPI(cfg.gc_display['spi'], baudrate=cfg.gc_display['baud'],
                        sck=Pin(cfg.gc_display['sck']), mosi=Pin(cfg.gc_display['mosi']))# use displayconfig from cfg
        
        self.Screen = Display(self.spi_display, dc=Pin(cfg.gc_display['dc']), cs=Pin(cfg.gc_display['cs']),
                              rst=Pin(cfg.gc_display['rst']), width = cfg.gc_display['width'], height = cfg.gc_display['height'],
                              bgr = cfg.gc_display['bgr'], gamma = cfg.gc_display['gamma'], rotation = cfg.gc_display['rotation'])
        
        self.backlight = Pin(cfg.gc_display['backlight'], Pin.OUT)
        self.backlight.on()
        
        self.spi_touch = SPI(cfg.gc_touch['spi'], baudrate=cfg.gc_touch['baud'], sck=Pin(cfg.gc_touch['sck']),
                        mosi=Pin(cfg.gc_touch['mosi']), miso=Pin(cfg.gc_touch['miso']))

        self.Touch = Touch(self.spi_touch, cs=Pin(cfg.gc_touch['cs']), int_pin=Pin(cfg.gc_touch['intPin']),
                           int_handler=self.touchscreen_press)
        
        self.Screen.clear(color565(255,255,255))
        
        
        #self.backlightPWM = PWM(self.backlight, freq=5000, duty_u16=32768)
        
        # Assign touch callbacks and draw elements on screen
        self.draw()

    
    def draw(self):
        ''' Draw text and assign a callback to touch event at rectangular area '''
        left = 25
        top = 25
        i = 0
        items = []
        for game in cfg.gc_games:
            
            text = cfg.gc_games[game]['name']
            self.Screen.draw_text8x8(left, top, text,
                                 color565(0, 0, 255), color565(255, 255, 255))
            items.append(self.TouchArea(self, (left-2), (top-2), 15 + 8 * len(text), 20, True))
            self.addTouchItem(items[i], cfg.gc_games[game])
            top += 25
            
            i += 1

        ''' Draw shutdown icon and bind callback to it '''
        a = 5    # Move the icon
        b = 190	 # Move the icon
        self.Screen.fill_circle(300 - a, 220 - b, 18, color565(0, 0, 0))
        self.Screen.fill_circle(300 - a, 220 - b, 15, color565(255, 255, 255))
        self.Screen.fill_rectangle(295 - a, 197 - b, 10, 20, color565(255, 255, 255))
        self.Screen.fill_rectangle(298 - a, 197 - b, 4, 20, color565(0, 0, 0))
        
        item3 = self.TouchArea(self, 300 - a - 20, 220 - b - 20, 40, 40)
        restart = {"name":"restart"}
        self.addTouchItem(item3, restart)
        
    def loadGame(self, game):
        if game['name'] == "restart":
            self.shutdown()
            return True;
        src = game['source']
        oGame = self.load_module(src)
        this = self
        lGame = oGame.pndGame()
        rtGame = lGame.gameRuntime(this)
        rtGame.setup()
        rtGame.run()
        print('loadGame: ' + game['name'])
        pass
    
    def load_module(self, module):

    # module_path = "mypackage.%s" % module
        module_path = module

        if module_path in sys.modules:
            return sys.modules[module_path]

        return __import__(module_path, module)

    def addTouchItem(self, item, cb):
        self.Touch_items.append(item)
        self.Touch_callbacks.append(cb)
        
    def shutdown(self):
        print('Shutdown.')
        self.spi_touch.deinit()
        #self.backlightPWM.deinit()
        
        self.backlight.off()
        self.Screen.cleanup()
        self.rtCB.Running = False
        sys.exit(0)
        
    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        x, y = y, x
        

        if self.mark_touch:
            self.Screen.fill_circle(x, y, 4, color_rgb(155, 155, 155))
            self.Screen.draw_circle(x, y, 4, color_rgb(255, 255, 255))
        
        
        if len(self.Touch_items) > 0:
            for i, item in enumerate(self.Touch_items):
                if x in item.TouchX and y in item.TouchY:
                    self.loadGame(self.Touch_callbacks[i])
 
 
                    
    class TouchArea:
        ''' Bind callback to rectangular touch area'''
        def __init__(self, parent, x, y, w, h, draw = False):
            self.parent = parent
            self.x = x
            self.y = y
            self.width = w
            self.height = h
            
            self.TouchX = range(self.x, self.x + self.width)
            self.TouchY = range(self.y, self.y + self.height)
            
            if draw is True:
                self.draw()
        
        ''' Draw the outline of the touch area '''
        def draw(self):
            self.color = color_rgb(70, 0, 0)
            
            for i in range(2):
                self.parent.Screen.draw_rectangle(self.x+i, self.y+i,
                                               self.width-2*i, self.height-2*i,
                                               color_rgb(255, 0, 0))        
        
