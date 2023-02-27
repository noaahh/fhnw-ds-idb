import time
import board

import tm1637lib
import adafruit_dht

from digitalio import DigitalInOut, Direction, Pull
import analogio
import pwmio

# Constants
INTERVAL = 1

# Buzzer
buzzer = pwmio.PWMOut(board.D5, variable_frequency=True)
buzzer.duty_cycle = 2**9

# LCD display
display = tm1637lib.Grove4DigitDisplay(board.A2, board.A3) # nRF52840 D9, D10, Grove D4
colon = True

# Melody to play on the buzzer with dynamic tempo (bpm)
melody = [
    (262, 500), (294, 500), (330, 500), (349, 350), (392, 150), (440, 500), (494, 350), (523, 150),
    (523, 500), (494, 500), (440, 500), (392, 350), (349, 150), (330, 500), (294, 350), (262, 150),
    (262, 500), (294, 500), (330, 500), (349, 350), (392, 150), (440, 500), (494, 350), (523, 150),
    (523, 500), (494, 500), (440, 500), (392, 350), (349, 150), (330, 500), (294, 350), (262, 150),
    (262, 500), (294, 500), (330, 500), (349, 350), (392, 150), (440, 500), (494, 350), (523, 150)]

for note in melody:
    buzzer.frequency = note[0]
    time.sleep(note[1] / 1000)
