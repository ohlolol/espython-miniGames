from ili9341 import Display, color565
from xpt2046 import Touch
from machine import Pin, SPI
from pndSRC import pndIFGame
import machine
import time
import random

def color_rgb(r, g, b):
    return color565(r, g, b)

class SnakeGame:
    def __init__(self, screen, touch):
        self.screen = screen
        self.touch = touch
        self.grid_size = 10
        self.width = 12  # 120 / 10
        self.height = 12  # 120 / 10
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)  # Startet nach rechts
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.offset_x = 20
        self.offset_y = 20
        self.colors = {
            'background': color_rgb(0, 0, 0),
            'snake': color_rgb(0, 255, 0),
            'food': color_rgb(255, 0, 0),
            'text': color_rgb(255, 255, 255),
            'border': color_rgb(255, 255, 255),
            'button': color_rgb(100, 100, 100),
            'button_active': color_rgb(200, 200, 200)
        }
        self.game_started = False  # Spiel startet erst nach Berührung

    def generate_food(self):
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food

    def draw_square(self, x, y, color):
        self.screen.fill_rectangle(
            self.offset_x + x * self.grid_size,
            self.offset_y + y * self.grid_size,
            self.grid_size,
            self.grid_size,
            color
        )

    def draw_board(self):
        # Zeichne den weißen Rand um das Spielfeld
        self.screen.draw_rectangle(self.offset_x - 2, self.offset_y - 2, 124, 124, self.colors['border'])
        self.screen.fill_rectangle(self.offset_x, self.offset_y, 120, 120, self.colors['background'])
        
        # Zeichne die Schlange
        for segment in self.snake:
            self.draw_square(segment[0], segment[1], self.colors['snake'])
        
        # Zeichne das Futter
        self.draw_square(self.food[0], self.food[1], self.colors['food'])

    def update(self):
        if self.game_over:
            return

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake):
            self.game_over = True
            self.draw_game_over()
            time.sleep(2)  # Kurze Pause, bevor das System zurückgesetzt wird
            machine.reset()  # System zurücksetzen
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.draw_board()
        self.draw_score()

    def draw_score(self):
        self.screen.fill_rectangle(0, 0, 320, 20, self.colors['background'])
        self.screen.draw_text8x8(10, 5, f"Score: {self.score}", self.colors['text'], self.colors['background'])

    def draw_game_over(self):
        self.screen.fill_rectangle(0, 220, 320, 20, self.colors['background'])
        self.screen.draw_text8x8(50, 220, "Game Over!", self.colors['text'], self.colors['background'])

    def reset_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.draw_board()
        self.draw_score()

    def set_direction(self, dx, dy):
        # Verhindere, dass die Schlange sich in die entgegengesetzte Richtung bewegt
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

class TouchScreen:
    def __init__(self, rtCB):
        self.rtCB = rtCB
        self.spi_display = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(13))
        self.screen = Display(self.spi_display, dc=Pin(2), cs=Pin(15), rst=Pin(15), width=320, height=240, rotation=270)
        self.spi_touch = SPI(2, baudrate=1000000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
        self.touch = Touch(self.spi_touch, cs=Pin(33), int_pin=Pin(36), int_handler=self.touchscreen_press)
        self.Touch_items = []
        self.Touch_callbacks = []
        self.snake_game = None  # Initialisiere snake_game als None
        self.game_started = False  # Spiel startet erst nach Berührung

    class TouchArea:
        def __init__(self, parent, x, y, w, h, draw=False):
            self.parent = parent
            self.x = x
            self.y = y
            self.width = w
            self.height = h
            self.TouchX = range(self.x, self.x + self.width)
            self.TouchY = range(self.y, self.y + self.height)
            if draw:
                self.draw()

        def draw(self):
            self.parent.screen.draw_rectangle(self.x, self.y, self.width, self.height, color_rgb(100, 100, 100))
            self.parent.screen.draw_rectangle(self.x + 1, self.y + 1, self.width - 2, self.height - 2, color_rgb(200, 200, 200))

    def setup(self):
        self.backlight = Pin(21, Pin.OUT)
        self.backlight.on()

    def draw_control_pad(self):
        # Steuerkreuz Buttons (20x20 Pixel)
        button_size = 20
        button_offset_x = 160  # Rechts neben dem Spielfeld
        button_offset_y = 60   # Vertikale Position

        # Links
        self.addTouchItem(self.TouchArea(self, button_offset_x, button_offset_y + button_size, button_size, button_size, draw=True),
                          lambda x: self.start_game_and_set_direction(-1, 0))
        self.screen.draw_text8x8(button_offset_x + 5, button_offset_y + button_size + 5, "<", color_rgb(255, 255, 255), color_rgb(100, 100, 100))

        # Rechts
        self.addTouchItem(self.TouchArea(self, button_offset_x + button_size, button_offset_y + button_size, button_size, button_size, draw=True),
                          lambda x: self.start_game_and_set_direction(1, 0))
        self.screen.draw_text8x8(button_offset_x + button_size + 5, button_offset_y + button_size + 5, ">", color_rgb(255, 255, 255), color_rgb(100, 100, 100))

        # Oben
        self.addTouchItem(self.TouchArea(self, button_offset_x + button_size // 2, button_offset_y, button_size, button_size, draw=True),
                          lambda x: self.start_game_and_set_direction(0, -1))
        self.screen.draw_text8x8(button_offset_x + button_size // 2 + 5, button_offset_y + 5, "^", color_rgb(255, 255, 255), color_rgb(100, 100, 100))

        # Unten
        self.addTouchItem(self.TouchArea(self, button_offset_x + button_size // 2, button_offset_y + 2 * button_size, button_size, button_size, draw=True),
                          lambda x: self.start_game_and_set_direction(0, 1))
        self.screen.draw_text8x8(button_offset_x + button_size // 2 + 5, button_offset_y + 2 * button_size + 5, "v", color_rgb(255, 255, 255), color_rgb(100, 100, 100))

    def start_game_and_set_direction(self, dx, dy):
        if not self.game_started:
            self.game_started = True
            self.snake_game.game_started = True
        self.snake_game.set_direction(dx, dy)

    def run(self):
        self.snake_game = SnakeGame(self.screen, self.touch)  # Initialisiere snake_game hier
        self.snake_game.draw_board()
        self.snake_game.draw_score()
        self.draw_control_pad()  # Zeichne das Steuerkreuz nach der Initialisierung von snake_game

        # Warte auf Spielstart (Berührung einer Pfeiltaste)
        while not self.game_started:
            time.sleep(0.1)

        # Hauptspielschleife
        while not self.snake_game.game_over:
            self.snake_game.update()
            time.sleep(0.2)

    def stop(self):
        print('Shutdown.')
        self.spi_touch.deinit()
        self.backlight.off()
        self.screen.cleanup()
        self.rtCB.Running = False
        machine.reset()

    def addTouchItem(self, item, cb):
        self.Touch_items.append(item)
        self.Touch_callbacks.append(cb)

    def touchscreen_press(self, x, y):
        x, y = y, x
        if len(self.Touch_items) > 0:
            for i, item in enumerate(self.Touch_items):
                if x in item.TouchX and y in item.TouchY:
                    self.Touch_callbacks[i](i)

class pndGame(pndIFGame):
    name = "Snake"
    def gameRuntime(self, rtCB):
        self.rtCB = rtCB
        return TouchScreen(rtCB)