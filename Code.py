
import board
import usb_hid
import keypad
import busio
import time
import adafruit_ssd1306
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kb = Keyboard(usb_hid.devices)

pins = [
    board.GP0, board.GP1, board.GP2, board.GP3,
    board.GP4, board.GP5, board.GP6, board.GP7,
    board.GP8, board.GP9, board.GP10, board.GP11
]

buttons = keypad.Keys(pins, value_when_pressed=False, pull=True)

i2c = busio.I2C(scl=board.GP12, sda=board.GP13)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

shortcuts = [
    (Keycode.CONTROL, Keycode.C),
    (Keycode.CONTROL, Keycode.V),
    (Keycode.CONTROL, Keycode.Z),
    (Keycode.CONTROL, Keycode.S),
    (Keycode.ALT, Keycode.TAB),
    (Keycode.CONTROL, Keycode.T),
    (Keycode.CONTROL, Keycode.W),
    (Keycode.CONTROL, Keycode.R),
    (Keycode.CONTROL, Keycode.F),
    (Keycode.CONTROL, Keycode.A),
    (Keycode.CONTROL, Keycode.X),
    (Keycode.ENTER,)
]

shortcut_names = [
    "Copy", "Paste", "Undo", "Save",
    "Alt+Tab", "New Tab", "Close Tab", "Refresh",
    "Find", "Select All", "Cut", "Enter"
]

held_keys = {10: Keycode.BACKSPACE}

last_action = ""
action_until = 0

while True:
    event = buttons.events.get()
    now_ticks = time.monotonic()

    if event:
        key = event.key_number

        if event.pressed:
            if key in held_keys:
                kb.press(held_keys[key])
                last_action = "Backspace"
            else:
                kb.send(*shortcuts[key])
                last_action = shortcut_names[key]

            action_until = now_ticks + 1

        if event.released and key in held_keys:
            kb.release(held_keys[key])

    oled.fill(0)
    oled.text("MACRO PAD", 0, 0)

    if now_ticks < action_until:
        oled.text("Shortcut:", 0, 12)
        oled.text(last_action, 0, 24)
    else:
        now = time.localtime()
        oled.text(
            "{:02d}:{:02d}:{:02d}".format(
                now.tm_hour, now.tm_min, now.tm_sec
            ),
            0, 12
        )
        oled.text(
            "{:02d}/{:02d}/{}".format(
                now.tm_mday, now.tm_mon, now.tm_year
            ),
            0, 24
        )

    oled.show()
    time.sleep(0.05)
