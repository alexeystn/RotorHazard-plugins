'''LED visual effects'''

from eventmanager import Evt
from led_event_manager import LEDEffect, LEDEvent, Color, ColorVal, ColorPattern, effect_delay
import time
import datetime


class Matrix:

    characters = {
        0: [ [0, 1, 1, 1, 0],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [0, 1, 1, 1, 0] ],

        1: [ [0, 0, 1, 0, 0],
             [0, 1, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 1, 1, 1, 0] ],

        2: [ [0, 1, 1, 1, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 1, 0],
             [0, 0, 1, 0, 0],
             [0, 1, 0, 0, 0],
             [1, 1, 1, 1, 1] ],

        3: [ [0, 1, 1, 1, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 1, 1, 0],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [0, 1, 1, 1, 0] ],

        4: [ [0, 0, 0, 0, 1],
             [0, 0, 0, 1, 1],
             [0, 0, 1, 0, 1],
             [0, 1, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1] ],

        5: [ [1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [0, 1, 1, 1, 0] ],

        6: [ [0, 0, 1, 1, 0],
             [0, 1, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 1, 1, 1, 0],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [0, 1, 1, 1, 0] ],

        7: [ [1, 1, 1, 1, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 1, 0, 0, 0],
             [0, 1, 0, 0, 0] ],

        8: [ [0, 1, 1, 1, 0],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [0, 1, 1, 1, 0],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [0, 1, 1, 1, 0] ],

        9: [ [0, 1, 1, 1, 0],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [0, 1, 1, 1, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 1, 0],
             [0, 1, 1, 0, 0] ],

      'G': [ [0, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 0, 0, 0, 0, 0, 0],
             [1, 1, 0, 0, 1, 1, 1, 1],
             [1, 1, 0, 0, 1, 1, 1, 1],
             [1, 1, 0, 0, 0, 0, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 0] ],

      'O': [ [0, 1, 1, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 0, 0, 0, 0, 1, 1],
             [1, 1, 0, 0, 0, 0, 1, 1],
             [1, 1, 0, 0, 0, 0, 1, 1],
             [1, 1, 0, 0, 0, 0, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 0] ],

      '!': [ [1, 1],
             [1, 1],
             [1, 1],
             [1, 1],
             [1, 1],
             [0, 0],
             [1, 1],
             [1, 1] ],        
    }

    def __init__(self, strip, color):
        self.strip = strip
        self.color = color
        self.matrix = [[0] * 40 for _ in range(8)]

    def clear(self):
        for x in range(40):
            for y in range(8):
                self.matrix[y][x] = 0

    def putCharacter(self, char, position):
        for y in range(8):
            for x in range(len(self.characters[char][0])):
                self.matrix[y][position+x] = self.characters[char][y][x]

    def putColon(self, position):
        self.matrix[2][position] = 1
        self.matrix[5][position] = 1

    def display(self, args):

        if args['RHAPI'].config.get_item('LED', 'PANEL_ROTATE'):
            self.matrix = [row[::-1] for row in self.matrix[::-1]]

        for x in range(40):
            for y in range(8):
                pos = x * 8 + y
                if args['RHAPI'].config.get_item('LED', 'INVERTED_PANEL_ROWS'):
                    if x % 2:
                        pos = x * 8 + (8 - y - 1)
                if self.matrix[y][x] == 1:
                    self.strip.setPixelColor(pos, self.color)
                else:
                    self.strip.setPixelColor(pos, ColorVal.NONE)


def realTimeClock(args):

    if 'strip' in args:
        strip = args['strip']
    else:
        return False
 
    if args['RHAPI'].config.get_item('LED', 'LED_COUNT') < 8*40:
        return False

    if args['RHAPI'].config.get_item('LED', 'CLOCK_COLOR'):
        color_name = args['RHAPI'].config.get_item('LED', 'CLOCK_COLOR')
        if color_name == 'red':
            color = Color(255, 0, 0)
        elif color_name == 'green':
            color = Color(0, 255, 0)
        elif color_name == 'blue':
            color = Color(0, 0, 255)
        elif color_name == 'yellow':
            color = Color(255, 127, 0)
        else:
            color = Color(127, 127, 127)

    clock = Matrix(strip, color)
    new_time = int(time.time())

    while True:
        prev_time = new_time
        while prev_time == new_time:
            new_time = int(time.time())
            effect_delay(10, args)
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        
        clock.clear()

        clock.putCharacter(hour//10, 0)
        clock.putCharacter(hour%10, 6)
        #clock.putColon(12)
        clock.putCharacter(minute//10, 14)
        clock.putCharacter(minute%10, 20)
        #clock.putColon(26)
        clock.putCharacter(second//10, 28)
        clock.putCharacter(second%10, 34)

        clock.display(args) 
        effect_delay(10, args)
        strip.show()


def goText(args):

    if 'strip' in args:
        strip = args['strip']
    else:
        return False
 
    if args['RHAPI'].config.get_item('LED', 'LED_COUNT') < 8*40:
        return False

    text = Matrix(strip, args['color'])
    text.clear()
    text.putCharacter('G', 10)
    text.putCharacter('O', 19)
    text.putCharacter('!', 28)
    text.display(args)
    strip.show()


def discover():
    return [

    LEDEffect("Real Time Clock", realTimeClock, {
        'include': [LEDEvent.IDLE_DONE, LEDEvent.IDLE_READY, LEDEvent.IDLE_RACING]
        },
        {},
        name="realTimeClock",
    ),

    LEDEffect("GO!", goText, {
        'recommended': [Evt.RACE_START],
        'include': [Evt.RACE_START],
        'exclude': [Evt.ALL]
        }, {
        'pattern': ColorPattern.SOLID,
        'time': 4
        },
        name="go8",
    ),

    ]

def register_handlers(args):
    for led_effect in discover():
        args['register_fn'](led_effect)

def initialize(rhapi):
    rhapi.events.on(Evt.LED_INITIALIZE, register_handlers)
