import board
import busio
import digitalio
import adafruit_matrixkeypad
import neopixel
import adafruit_ssd1306
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# 1. OLED Setup (I2C)
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# 2. LED Setup (GPIO 0 / TX)
pixels = neopixel.NeoPixel(board.TX, 16, brightness=0.2)

# 3. Keyboard Matrix Setup
# Pins match your schematic: Rows (26, 27, 28, 29), Cols (3, 4, 2, 1)
cols = [digitalio.DigitalInOut(p) for p in (board.D3, board.D4, board.D2, board.D1)]
rows = [digitalio.DigitalInOut(p) for p in (board.A0, board.A1, board.A2, board.A3)]

keys = (
    (1, 2, 3, 4),
    (5, 6, 7, 8),
    (9, 10, 11, 12),
    (13, 14, 15, 16)
)

keypad = adafruit_matrixkeypad.MatrixKeypad(rows, cols, keys)

# 4. HID Keyboard Setup
kbd = Keyboard(usb_hid.devices)


def update_display(text):
    display.fill(0)
    display.text("CloudPad Active", 0, 0, 1)
    display.text(f"Last Key: {text}", 0, 20, 1)
    display.show()


update_display("None")

while True:
    keys_pressed = keypad.pressed_keys
    if keys_pressed:
        key = keys_pressed[0]
        update_display(str(key))

        # Example Macro Logic
        if key == 1:
            pixels.fill((255, 0, 0))  # Red
            kbd.send(Keycode.CONTROL, Keycode.C)  # Copy
        elif key == 2:
            pixels.fill((0, 255, 0))  # Green
            kbd.send(Keycode.CONTROL, Keycode.V)  # Paste
        else:
            pixels.fill((0, 0, 255))  # Blue default

        pixels.show()