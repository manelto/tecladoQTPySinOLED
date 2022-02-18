#circuitPython 7.1.1
#lib:
#   adafruit_hid
#   adafruit_neokey
#   adafruit_seesaw

import time
import board
from rainbowio import colorwheel
import busio
from adafruit_neokey.neokey1x4 import NeoKey1x4
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize Keybaord
kbd = Keyboard(usb_hid.devices)


# use STEMMA I2C bus on RP2040 QT Py
i2c_bus = busio.I2C(board.SCL1, board.SDA1)

# Create a NeoKey object
neokey1 = NeoKey1x4(i2c_bus, addr=0x30)
#  you solder the jumpers "closed" by connecting the two pads.
#If only A0 is soldered closed, the address is 0x30 + 1 = 0x31
neokey2 = NeoKey1x4(i2c_bus, addr=0x31)

#color = 0xRRGGBB
colorKeys = [
    (neokey1, 0, 0xFF0000), #RED
    (neokey1, 1, 0xFFFFFF), #WHITE
    (neokey1, 2, 0x0000FF), #BLUE
    (neokey1, 3, 0x00FF00), #GREEN
    (neokey2, 0, 0xFF0000), #RED
    (neokey2, 1, 0xFF0000), #RED
    (neokey2, 2, 0xFF0000), #RED
    (neokey2, 3, 0x00FF00), #GREEN
]

state= [False, False, False, False, False, False, False, False]

off = (0, 0, 0)


# -----------------------------------------------------------------------------------------------------------------------------
# Keystroke set
# the value -1 signals that the set of previous keystrokes are released

# Conjunto de pulsaciones
# El valor -1 ordena un release entre pulsaciones.
# -----------------------------------------------------------------------------------------------------------------------------

# keys for vba (run, save, debuger,intro)(run over functions, run out functions, step to step, pause)

keys = [
          [Keycode.F5],[Keycode.CONTROL,Keycode.S,-1,Keycode.CONTROL,Keycode.S,Keycode.G],[Keycode.LEFT_ALT,Keycode.F11],[Keycode.ENTER],
          [Keycode.SHIFT,Keycode.F8],[Keycode.SHIFT,Keycode.CONTROL,Keycode.F8],[Keycode.F8],[Keycode.CONTROL,Keycode.PAUSE],
];

# Check each button, if pressed, light up the matching NeoPixel!
while True:

    for i in range(8):
        neokey, key_number, color = colorKeys[i]
        kbd.release_all()

        if neokey[key_number] and not state[i]:
            print("Button", i)
            neokey.pixels[key_number] = color
            x = 0
            while x<len(keys[i]):
                if keys[i][x]<0:
                    kbd.release_all()
                if keys[i][x]>0:
                    kbd.press(keys[i][x])
                print(keys[i][x])
                x += 1
            time.sleep(.1)

            state[i] = True
        else:
            neokey.pixels[key_number] = off
            state[i]= False


