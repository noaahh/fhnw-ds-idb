from pulseio import PulseIn
import time
import board
from digitalio import DigitalInOut, Direction

pulsein = PulseIn(board.D5)

pulsein.clear()
pulsein.resume()
pulsein.pause()

while True:
    pulsein.resume(100)
    pulsein.pause()

    if len(pulsein) > 0:
        print(pulsein[0])
    
    pulsein.clear()