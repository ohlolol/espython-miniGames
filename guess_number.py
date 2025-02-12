import random as rnd
## import tkinter as tk		## Ohlolol: not needet -> goig to HardwareDisplay


## import display dirver
from ili9341 import Display, color565
from xpt2046 import Touch

## import kernel modules
from machine import Pin, SPI, PWM

## import array
import array

## import machine
import machine

## import time
import time

## import Cpnfiguration
from pndConfig import tasks as cfg # get Configuration

## import pndGame Interface
from pndSRC import pndIFGame

class Game:
    
    ###! Ohlolol we need to store the text to display in our parrent object to dynamicaly add numbers
    userInput = ""
    
    ###! Ohlolol we need to know if the game is done
    gameOver = False
    
    # --------------------------------------------------
    # B A S I C   E X E C U T I O N   C O N D I T I O N S
    # --------------------------------------------------
    def __init__(self, rtCB): ## Ohlolol: "root" removed, its from tk; "rtCB" added, We need an object to talk with the menu
        ## not needed anymore
        #root.title("Zahlenratespiel")
        #root.geometry("320x240")
        #root.resizable(False, False)
        #root.configure(bg="gray0")
        #root.wm_attributes("-fullscreen", True)
        
        
        ## init display and touch
        self.rtCB = rtCB
        self.mark_touch = False # True, False --> Show touch coordinates
        self.Touch_items = []
        self.Touch_callbacks = []
        ## init display
        self.spi_display = SPI(cfg.gc_display['spi'], baudrate=cfg.gc_display['baud'],
                        sck=Pin(cfg.gc_display['sck']), mosi=Pin(cfg.gc_display['mosi']))# use displayconfig from cfg
        
        self.Screen = Display(self.spi_display, dc=Pin(cfg.gc_display['dc']), cs=Pin(cfg.gc_display['cs']),
                              rst=Pin(cfg.gc_display['rst']), width = cfg.gc_display['width'], height = cfg.gc_display['height'],
                              bgr = cfg.gc_display['bgr'], gamma = cfg.gc_display['gamma'], rotation = cfg.gc_display['rotation'])
        
        ## turn backlight on
        self.backlight = Pin(cfg.gc_display['backlight'], Pin.OUT)
        self.backlight.on()
        
        ## init touch
        self.spi_touch = SPI(cfg.gc_touch['spi'], baudrate=cfg.gc_touch['baud'], sck=Pin(cfg.gc_touch['sck']),
                        mosi=Pin(cfg.gc_touch['mosi']), miso=Pin(cfg.gc_touch['miso']))

        self.Touch = Touch(self.spi_touch, cs=Pin(cfg.gc_touch['cs']), int_pin=Pin(cfg.gc_touch['intPin']),int_handler=self.touchscreen_press)
        
        ## flush screen (white)
        self.Screen.clear(color565(255,255,255))
                
        
        
        self.rng = rnd.randrange(1, 100)
        print(f"Zufallsgenerator erzeugt die Zahl {self.rng}")
        
        
        ## Ohlolol: we dont have tk class; output should not be generated in initialsation
        ##self.message = tk.StringVar()
        ##self.message.set("Drücke im Anschluss auf den OK Button")
        
        ## Ohlolol: never start the loop in initialsation
        ##self.setup_ui()

    # --------------------------------------------------
    # G R A P H I C A L   U S E R   I N T E R F A C E
    # --------------------------------------------------
    def setup_ui(self):
        ## Ohlolol: port to display
        # H E A D E R   F R A M E
        #header_frame = tk.Frame(root, bg="gray10")
        #header_frame.pack(side="top", fill="x")
        #tk.Label(header_frame, text="Zahlenratespiel", bg="gray10", fg="white").pack(pady=5)
        
        # draw the headder
        text = 'Zahlenratespiel'
        self.Screen.draw_text8x8(25, 25, text,
                                 color565(32, 32, 32), color565(255, 255, 255)) ## RGB: Grey
       

        ## Ohlolol: port to display
        # M A I N   F R A M E
        #main_frame = tk.Frame(root, bg="gray5")
        #main_frame.pack(fill="both", padx=5, pady=5)
        #tk.Label(main_frame, bg="gray5", fg="white", text="Gib eine Zahl ein").pack()

        # draw the mainframe
        text = 'Gib eine Zahl ein'
        self.Screen.draw_text8x8(25, 75, text,
                                 color565(32, 32, 32), color565(255, 255, 255)) ## RGB: another Grey
        
        ## Ohlolol: no tk, already drawed on display
        #self.main_entry = tk.Entry(main_frame)
        #self.main_entry.pack()
        
        ## Ohlolol: no tk -> draw "ok" button
        #tk.Label(main_frame, bg="gray5", fg="white", textvariable=self.message).pack()
        #tk.Button(main_frame, text="OK" ,command=self.check_number).pack()

        # B U T T O N   F R A M E
        #button_frame = tk.Frame(root, bg="gray5")
        #button_frame.pack()

        # draw "ok" button
        text = 'OK'
        self.Screen.draw_text8x8(25, 125, text,
                                 color565(32, 32, 32), color565(255, 255, 255)) ## RGB: yet another Grey
        
        # bind method "check_number" to toucharea over "ok" button
        oNumb = myNumb(99)
        btnOk = self.TouchArea(self, (20), (125), 75, 75, False)
        self.addTouchItem(btnOk, oNumb)
        
        ## Ohlolol: ported to display; WHY no LOOP?
        # B U T T O N S
        #n0 = tk.Button(button_frame, width=2, height=1, text="0", command=lambda: self.add_numbers(0)) 
        #n1 = tk.Button(button_frame, width=2, height=1, text="1", command=lambda: self.add_numbers(1))
        #n2 = tk.Button(button_frame, width=2, height=1, text="2", command=lambda: self.add_numbers(2))
        #n3 = tk.Button(button_frame, width=2, height=1, text="3", command=lambda: self.add_numbers(3))
        #n4 = tk.Button(button_frame, width=2, height=1, text="4", command=lambda: self.add_numbers(4))
        #n5 = tk.Button(button_frame, width=2, height=1, text="5", command=lambda: self.add_numbers(5))
        #n6 = tk.Button(button_frame, width=2, height=1, text="6", command=lambda: self.add_numbers(6))
        #n7 = tk.Button(button_frame, width=2, height=1, text="7", command=lambda: self.add_numbers(7))
        #n8 = tk.Button(button_frame, width=2, height=1, text="8", command=lambda: self.add_numbers(8))
        #n9 = tk.Button(button_frame, width=2, height=1, text="9", command=lambda: self.add_numbers(9))

        # B U T T O N S   G R I D
        #n0.grid(column=0, row=0)
        #n1.grid(column=1, row=0)
        #n2.grid(column=2, row=0)
        #n3.grid(column=3, row=0)
        #n4.grid(column=4, row=0)
        #n5.grid(column=0, row=1)
        #n6.grid(column=1, row=1)
        #n7.grid(column=2, row=1)
        #n8.grid(column=3, row=1)
        #n9.grid(column=4, row=1)
        
        
        # add butons with logic
        numbs = {1,2,3,4,5,6,7,8,9,0}
        btn = []
        x = 100
        y = 15
        for numb in numbs: ## Looping baby d(-.-)b
                    # draw inside mainframe
                    text = str(numb)
                    oNumb = myNumb(numb)
                    self.Screen.draw_text8x8(y, x, text, color565(255, 255, 255), color565(153, 0, 153)) ## RGB: i like purple
                    
                    # add touch with method call
                    btn.append(self.TouchArea(self,(y-5), (x-5), 25, 25, True))
                    self.addTouchItem(btn[numb], oNumb)
                    y += 30
        ## Ohlolol: ported to display
        # F O O T E R   F R A M E
        #footer_frame = tk.Frame(root, bg="gray10")
        #footer_frame.pack(side="bottom", fill="x")
        #tk.Label(footer_frame, text="©2025 Schmacht Games", bg="gray10", fg="white").pack(padx=5)

        
        # draw footer 
        text = '\u00A9 2025 Schmacht Games'
        self.Screen.draw_text8x8(25, 215, text,
                                 color565(32, 32, 32), color565(255, 255, 255)) ## RGB: yet another Grey        
        
        ###! Ohlolol: implement Shutdown Button
        ''' Draw shutdown icon and bind callback to it '''
        a = 5    # Move the icon
        b = 190	 # Move the icon
        self.Screen.fill_circle(300 - a, 220 - b, 18, color565(0, 0, 0))
        self.Screen.fill_circle(300 - a, 220 - b, 15, color565(255, 255, 255))
        self.Screen.fill_rectangle(295 - a, 197 - b, 10, 20, color565(255, 255, 255))
        self.Screen.fill_rectangle(298 - a, 197 - b, 4, 20, color565(0, 0, 0))
        
        item3 = self.TouchArea(self, 300 - a - 20, 220 - b - 20, 40, 40)
        oStop = myNumb(69)
        self.addTouchItem(item3, oStop)
    # --------------------------------------------------
    # G A M E P L A Y   M E C H A N I C S
    # --------------------------------------------------
    def add_numbers(self, number): ## Ohlolol: since we dont have tk class we need to draw it our self. this gets wild...
        #current = self.main_entry.get()
        #self.main_entry.delete(0, tk.END)
        #self.main_entry.insert(0, current + str(number))
        
        ###! Ohlolol we need to store the text to display in our parrent object to dynamicaly add numbers
        newInput = self.userInput
        newInput += str(number)
        print(newInput)
        self.userInput = newInput
        
        
        # clear output screen
        self.Screen.fill_rectangle(10, 75, 300, 20, color565(255, 255, 255))
        
        # print number
        self.Screen.draw_text8x8(25, 75, newInput,
                                 color565(32, 32, 32), color565(255, 255, 255)) ## RGB: another Grey


    def check_number(self):
        try:
            ## Ohlolol: ported to display
            #input = int(self.main_entry.get())
            #self.main_entry.delete(0, tk.END)
            print(f"Eingegebene Zahl wurde ausgelesen: {self.userInput}")
            #if input < 1 or input > 100:
            #if not (1 <= input <= 100):
                #self.update_message("Bitte gib eine Zahl zwischen 1 und 100 ein")
            #elif input < self.rng:
                #self.update_message(f"Die gesuchte Zahl ist größer als {input}")
            #elif input > self.rng:
                #self.update_message(f"Die gesuchte Zahl ist kleiner als {input}")
            #else:
                #self.update_message(f"Du hast die gesuchte Zahl erraten: {input}")
            
            # get input
            uInput = int(self.userInput)
            
            # math
            if uInput < 1 or uInput > 100:
                #self.update_message("Bitte gib eine Zahl zwischen 1 und 100 ein")
                ## Ohlolol: message to long, we try shorter string
                self.update_message("only 1-100 alowed")
            elif uInput < self.rng:
                #self.update_message("Die gesuchte Zahl ist groesser als deine")
                ## Ohlolol: message to long, we try shorter string
                self.update_message("the number is bigger")
            elif uInput > self.rng:
                #self.update_message("Die gesuchte Zahl ist kleiner als deine")
                ## Ohlolol: message to long, we try shorter string
                self.update_message("the number is smaler")
            else:
                #self.update_message("Du hast die gesuchte Zahl erraten!")
                ## Ohlolol: message to long, we try shorter string
                self.update_message("number found, you win!")
            
            
            
            ## Ohlolol: we need to reset the input
            self.userInput = ""
            
        except ValueError:
                self.update_message("Gib eine gueltige Zahl ein")

    def update_message(self, text):
        print(text)
        ## Ohlolol: ported to display
        #self.message.set(text)
        
        # clear output screen
        self.Screen.fill_rectangle(10, 75, 300, 20, color565(255, 255, 255))
        #self.Screen.fill_rectangle(10, 75, 300, 20, color565(0, 0, 0))
        #text = "TEST"
        #time.sleep(1)
        # draw message
        self.Screen.draw_text8x8(25, 75, text,
                                 color565(32, 32, 32), color565(255, 255, 255)) ## RGB: another Grey
        #time.sleep(1)
        
# --------------------------------------------------
# P R O C E S S   L O G I C
# --------------------------------------------------

## Ohlolol: not needet anymore
#if __name__ == "__main__":
    #root = tk.Tk()
    #app = Game(root)
    #root.mainloop()
   
   


###! Ohlolol: Implement touch logics 
    def addTouchItem(self, item, cb):
        self.Touch_items.append(item)
        self.Touch_callbacks.append(cb)
        
    def touchscreen_press(self, x, y):
        """Verarbeitet Touch-Eingaben."""
        x, y = y, x
        if not self.gameOver:
            # Debug: Touch-Koordinaten anzeigen
            print(f"Touch coordinates: x={x}, y={y}")
            
            if len(self.Touch_items) > 0:
                for i, item in enumerate(self.Touch_items):
                    if x in item.TouchX and y in item.TouchY:
                        if self.Touch_callbacks[i].numb == 99:
                            #print("ok pressed")
                            #print(item.TouchX)
                            #print(item.TouchY)
                            self.check_number()
                            
                        elif self.Touch_callbacks[i].numb == 69: ## end game
                            self.stop()
                        else:
                            self.add_numbers(self.Touch_callbacks[i].numb)
                        

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

###! Implement generic "setup", "run" and "stop" method's
    def setup(self):
        ## not rly needet, all game logic is in check_number which is called by the "ok" button
        pass
        
    def run(self):    
        self.setup_ui()
        
    def stop(self):
        self.rtCB.Running = False
        print('Shutdown.')
        self.spi_touch.deinit() # touch off       
        self.backlight.off() # light off
        self.Screen.cleanup() # clear screen
        machine.reset()



    
## Ohlolol: implement pndGame Interface
class pndGame(pndIFGame):
    name = "number-guesser"
    def gameRuntime(self, rtCB):
        return Game(rtCB)
    
    
## Ohlolol: little helpers
    
    # object to hold a given number
class myNumb():
    def __init__(self, numb):
        self.numb = int(numb)
    
def color_rgb(r, g, b):
    return color565(r, g, b)