# Based on https://github.com/Seeed-Studio/grove.py/blob/master/grove/grove_4_digit_display.py licensed under MIT License

import time
import board
import digitalio
 
charmap = {
    '0': 0x3f,
    '1': 0x06,
    '2': 0x5b,
    '3': 0x4f,
    '4': 0x66,
    '5': 0x6d,
    '6': 0x7d,
    '7': 0x07,
    '8': 0x7f,
    '9': 0x6f,
    'A': 0x77,
    'B': 0x7f,
    'b': 0x7C,
    'C': 0x39,
    'c': 0x58,
    'D': 0x3f,
    'd': 0x5E,
    'E': 0x79,
    'F': 0x71,
    'G': 0x7d,
    'H': 0x76,
    'h': 0x74,
    'I': 0x06,
    'J': 0x1f,
    'K': 0x76,
    'L': 0x38,
    'l': 0x06,
    'n': 0x54,
    'O': 0x3f,
    'o': 0x5c,
    'P': 0x73,
    'r': 0x50,
    'S': 0x6d,
    'U': 0x3e,
    'V': 0x3e,
    'Y': 0x66,
    'Z': 0x5b,
    '-': 0x40,
    '_': 0x08,
    ' ': 0x00
}
 
ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7
 
 
class Grove4DigitDisplay(object):
    colon_index = 1
 
    def __init__(self, clk, dio, brightness=BRIGHT_DEFAULT):
        self.brightness = brightness
 
        self.clk = digitalio.DigitalInOut(clk)
        self.clk.direction = digitalio.Direction.OUTPUT
        self.dio = digitalio.DigitalInOut(dio)
        self.dio.direction = digitalio.Direction.OUTPUT
        
        self.data = [0] * 4
        self.show_colon = False
 
    def clear(self):
        self.show_colon = False
        self.data = [0] * 4
        self._show()
 
    def show(self, data):
        if type(data) is str:
            for i, c in enumerate(data):
                if c in charmap:
                    self.data[i] = charmap[c]
                else:
                    self.data[i] = 0
                if i == self.colon_index and self.show_colon:
                    self.data[i] |= 0x80
                if i == 3:
                    break
        elif type(data) is int:
            self.data = [0, 0, 0, charmap['0']]
            if data < 0:
                negative = True
                data = -data
            else:
                negative = False
            index = 3
            while data != 0:
                self.data[index] = charmap[str(data % 10)]
                index -= 1
                if index < 0:
                    break
                data = int(data / 10)
 
            if negative:
                if index >= 0:
                    self.data[index] = charmap['-']
                else:
                    self.data = charmap['_'] + [charmap['9']] * 3
        else:
            raise ValueError('Not support {}'.format(type(data)))
        self._show()
 
    def _show(self):
        with self:
            self._transfer(ADDR_AUTO)
 
        with self:
            self._transfer(STARTADDR)
            for i in range(4):
                self._transfer(self.data[i])
 
        with self:
            self._transfer(0x88 + self.brightness)
 
    def update(self, index, value):
        if index < 0 or index > 4:
            return
 
        if value in charmap:
            self.data[index] = charmap[value]
        else:
            self.data[index] = 0
 
        if index == self.colon_index and self.show_colon:
            self.data[index] |= 0x80
 
        with self:
            self._transfer(ADDR_FIXED)
 
        with self:
            self._transfer(STARTADDR | index)
            self._transfer(self.data[index])
 
        with self:
            self._transfer(0x88 + self.brightness)
 
 
    def set_brightness(self, brightness):
        if brightness > 7:
            brightness = 7
 
        self.brightness = brightness
        self._show()
 
    def set_colon(self, enable):
        self.show_colon = enable
        if self.show_colon:
            self.data[self.colon_index] |= 0x80
        else:
            self.data[self.colon_index] &= 0x7F
        self._show()
 
    def _transfer(self, data):
        for _ in range(8):
            self.clk.value = 0
            if data & 0x01:
                self.dio.value = 1
            else:
                self.dio.value = 0
            data >>= 1
            time.sleep(0.000001)
            self.clk.value = 1
            time.sleep(0.000001)

        self.clk.value = 0
        self.dio.value = 1
        self.clk.value = 1
        self.dio.direction = digitalio.Direction.INPUT
 
        while self.dio.value == 1:
            time.sleep(0.000001)

            if self.dio.value == 1:
                self.dio.direction = digitalio.Direction.OUTPUT
                self.dio.value = 0
                self.dio.direction = digitalio.Direction.INPUT

        self.dio.direction = digitalio.Direction.OUTPUT
 
    def _start(self):
        self.clk.value = 1
        self.dio.value = 1
        self.dio.value = 0
        self.clk.value = 0
 
    def _stop(self):
        self.clk.value = 0
        self.dio.value = 0
        self.clk.value = 1
        self.dio.value = 1
 
    def __enter__(self):
        self._start()
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop()