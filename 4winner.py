from ili9341 import Display, color565
from xpt2046 import Touch
from machine import Pin, SPI
from pndSRC import pndIFGame
import time

def color_rgb(r, g, b):
    return color565(r, g, b)

class ConnectFour:
    def __init__(self, screen, touch):
        self.screen = screen
        self.touch = touch
        self.board = [[0 for _ in range(7)] for _ in range(6)]  # 6 Reihen, 7 Spalten
        self.current_player = 1
        self.game_over = False
        self.cell_width = 20  # 50 % kleiner
        self.cell_height = 20  # 50 % kleiner
        self.offset_x = 20
        self.offset_y = 40  # Platz für Spieleranzeige oben
        self.colors = {0: color_rgb(255, 255, 255), 1: color_rgb(255, 0, 0), 2: color_rgb(0, 0, 255)}

    def draw_board(self):
        """Zeichnet das Spielfeld."""
        for row in range(6):
            for col in range(7):
                x = self.offset_x + col * self.cell_width
                y = self.offset_y + row * self.cell_height
                self.screen.fill_rectangle(x, y, self.cell_width, self.cell_height, self.colors[self.board[row][col]])
                self.screen.draw_rectangle(x, y, self.cell_width, self.cell_height, color_rgb(0, 0, 0))

    def drop_piece(self, col):
        """Lässt einen Spielstein in die angegebene Spalte fallen."""
        for row in range(5, -1, -1):  # Beginne von unten
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return True
        return False  # Spalte ist voll

    def check_win(self):
        """Überprüft, ob der aktuelle Spieler gewonnen hat."""
        # Horizontale Überprüfung
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == self.current_player and \
                   self.board[row][col+1] == self.current_player and \
                   self.board[row][col+2] == self.current_player and \
                   self.board[row][col+3] == self.current_player:
                    return True

        # Vertikale Überprüfung
        for row in range(3):
            for col in range(7):
                if self.board[row][col] == self.current_player and \
                   self.board[row+1][col] == self.current_player and \
                   self.board[row+2][col] == self.current_player and \
                   self.board[row+3][col] == self.current_player:
                    return True

        # Diagonale Überprüfung (positiv geneigt)
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.current_player and \
                   self.board[row+1][col+1] == self.current_player and \
                   self.board[row+2][col+2] == self.current_player and \
                   self.board[row+3][col+3] == self.current_player:
                    return True

        # Diagonale Überprüfung (negativ geneigt)
        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] == self.current_player and \
                   self.board[row-1][col+1] == self.current_player and \
                   self.board[row-2][col+2] == self.current_player and \
                   self.board[row-3][col+3] == self.current_player:
                    return True

        return False

    def switch_player(self):
        """Wechselt den Spieler."""
        self.current_player = 3 - self.current_player  # Wechsel zwischen Spieler 1 und 2

    def reset_game(self):
        """Setzt das Spiel zurück."""
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.game_over = False
        self.draw_board()

class TouchScreen:
    
    def __init__(self):
        self.spi_display = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(13))
        self.screen = Display(self.spi_display, dc=Pin(2), cs=Pin(15), rst=Pin(15), width=320, height=240, rotation=270)
        self.spi_touch = SPI(2, baudrate=1000000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
        self.touch = Touch(self.spi_touch, cs=Pin(33), int_pin=Pin(36), int_handler=self.touchscreen_press)
        self.Touch_items = []
        self.Touch_callbacks = []
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
    def setup(self):
        # Backlight aktivieren
        self.backlight = Pin(21, Pin.OUT)
        self.backlight.on()  # Backlight einschalten
        ''' Draw shutdown icon and bind callback to it '''
        a = 5    # Move the icon
        b = 190	 # Move the icon
        self.screen.fill_circle(300 - a, 220 - b, 18, color565(0, 0, 0))
        self.screen.fill_circle(300 - a, 220 - b, 15, color565(255, 255, 255))
        self.screen.fill_rectangle(295 - a, 197 - b, 10, 20, color565(255, 255, 255))
        self.screen.fill_rectangle(298 - a, 197 - b, 4, 20, color565(0, 0, 0))
        
        item3 = self.TouchArea(self, 300 - a - 20, 220 - b - 20, 40, 40)
        self.addTouchItem(item3, lambda x: self.stop())
        
    def run(self):    
        self.connect_four = ConnectFour(self.screen, self.touch)
        self.connect_four.draw_board()
        self.update_player_display()
        
    def stop(self):
        print('Shutdown.')
        self.spi_touch.deinit()
        #self.backlightPWM.deinit()
        
        self.backlight.off()
        self.screen.cleanup()
        
    def addTouchItem(self, item, cb):
        self.Touch_items.append(item)
        self.Touch_callbacks.append(cb)
        
    def update_player_display(self):
        """Aktualisiert die Anzeige, welcher Spieler am Zug ist."""
        self.screen.fill_rectangle(0, 0, 320, 20, color_rgb(255, 255, 255))  # Hintergrund löschen
        self.screen.draw_text8x8(10, 5, f"Player {self.connect_four.current_player}'s turn", color_rgb(0, 0, 0), color_rgb(255, 255, 255))

    def show_win_message(self):
        """Zeigt die Gewinnmeldung an."""
        self.screen.fill_rectangle(0, 220, 320, 20, color_rgb(255, 255, 255))  # Hintergrund löschen
        self.screen.draw_text8x8(50, 220, f"Player {self.connect_four.current_player} wins!", color_rgb(0, 0, 0), color_rgb(255, 255, 255))

    def touchscreen_press(self, x, y):
        """Verarbeitet Touch-Eingaben."""
        if not self.connect_four.game_over:
            # Debug: Touch-Koordinaten anzeigen
            print(f"Touch coordinates: x={x}, y={y}")
            
            # Spalte basierend auf der X-Koordinate berechnen (da das Display rotiert ist)
            col = (y - self.connect_four.offset_x) // self.connect_four.cell_height
            print(f"Calculated column: {col}")
            if len(self.Touch_items) > 0:
                for i, item in enumerate(self.Touch_items):
                    if y in item.TouchX and x in item.TouchY:
                        self.Touch_callbacks[i](i)
            if 0 <= col < 7:  # Nur gültige Spalten
                if self.connect_four.drop_piece(col):
                    self.connect_four.draw_board()
                    if self.connect_four.check_win():
                        self.connect_four.game_over = True
                        self.show_win_message()
                    else:
                        self.connect_four.switch_player()
                        self.update_player_display()

                
class pndGame(pndIFGame):
    name = "4-winner"
    def gameRuntime(self, rtCB):
        self.rtCB = rtCB
        return TouchScreen()

