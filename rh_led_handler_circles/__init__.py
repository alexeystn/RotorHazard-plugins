'''LED visual effects'''

from eventmanager import Evt
from led_event_manager import LEDEffect, LEDEvent, Color, ColorVal, ColorPattern, effect_delay
import time
import datetime


def decreaseBrightness(color):
    m = 255 - 3
    mask = (m * 256 + m) * 256 + m
    return (color & mask) >> 2


def drawCircle(args):

    colorLow = decreaseBrightness(args['color'])
    color = args['color']
    strip = args['strip']
    pos = args['position'] * args['size'] * args['size']

    if args['size'] == 8:
        full = {0: (3,5), 1: (2,6), 2: (1,7), 3: (1,7), 4: (2,6), 5: (3,5)}
        half = {0: [2,5], 1: [1,6], 2: [], 3: [], 4: [1,6], 5: [2,5]}
        pos += 8
        for x in range(6):
            for y in range(full[x][0], full[x][1]):
                strip.setPixelColor(pos+8*x+y, color)         
            for y in half[x]:
                strip.setPixelColor(pos+8*x+y, colorLow)
    elif args['size'] == 4:
        for x in range(4):
            # full = {0: (1,3), 1: (0,4), 2: (0,4), 3: (1,3)}
            full = {0: (0,4), 1: (0,4), 2: (0,4), 3: (0,4)}
            for y in range(full[x][0], full[x][1]):
                strip.setPixelColor(pos+4*x+y, color)
    else:
        strip.setPixelColor(pos, color) # handle other sizes


def showColorCircles(args):

    if 'strip' in args:
        strip = args['strip']
    else:
        return False
    
    if 'color' in args:
        color = args['color']
    else:
        color = ColorVal.WHITE

    size = args['RHAPI'].config.get_item('LED', 'LED_ROWS')
    args['size'] = size
    
    maxCount = strip.numPixels() // (size*size)

    if 'count' in args:
        count = args['count']
    else:
        count = maxCount
    if count > maxCount:
        count = maxCount

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, ColorVal.NONE)
         
    for i in range(count):
        if args['RHAPI'].config.get_item('LED', 'PANEL_ROTATE'):
            args['position'] = maxCount - 1 - i
        else:
            args['position'] = i
        drawCircle(args)
    strip.show()


def stagingCircles(args):

    triggers = args['staging_tones']
    args['count'] = 0
    args['effect_fn'](args)

    for i in range(0, triggers):
        args['count'] = i + 1
        effect_delay(1000, args)
        args['effect_fn'](args)


def discover():
    return [
        
    LEDEffect("Circles", showColorCircles, {
        'recommended': [Evt.RACE_START, Evt.RACE_STOP]
        }, {
        'pattern': ColorPattern.SOLID,
        'time': 4
        },
        name="showColorCircles",
    ),

    LEDEffect("Staging Circles", stagingCircles, {
        'manual': False,
        'include': [Evt.RACE_STAGE],
        'exclude': [Evt.ALL],
        'recommended': [Evt.RACE_STAGE]
        }, {
        'effect_fn': showColorCircles,
        'pattern': ColorPattern.SOLID,
        'ontime': 4,
        'steps': 0,
        'outSteps': 10,
        'time': 2
        },
        name="stagingCircles5",
    ),
    
    ]

def register_handlers(args):
    for led_effect in discover():
        args['register_fn'](led_effect)

def initialize(rhapi):
    rhapi.events.on(Evt.LED_INITIALIZE, register_handlers)
