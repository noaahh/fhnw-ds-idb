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
# buzzer = pwmio.PWMOut(board.D5, variable_frequency=True)

# LCD display
display = tm1637lib.Grove4DigitDisplay(board.A2, board.A3) # nRF52840 D9, D10, Grove D4
colon = True

# Rotary Angle Sensor
rotary = analogio.AnalogIn(board.A4)

# Button
button = DigitalInOut(board.A0)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Setup
dht = adafruit_dht.DHT11(board.D9)
    
show_temperature = False
# Main Loop
while True:

    # Read the rotary angle sensor
    print("Rotary angle sensor: {:d}".format(rotary.value))

    # Read the DHT11 sensor (temperature and humidity)
    start = time.time()
    t = time.localtime(start)
    try:
        # Read the temperature and convert it to integer
        temperature = int(round(dht.temperature))
        # Read the humidity and convert it to integer
        humidity = int(round(dht.humidity))
        
        # Print timestamp, temperatur, humidity in a nice readable format
        print("{:d}:{:02d}:{:02d},{:d},{:d}".format(
            t.tm_hour, t.tm_min, t.tm_sec, temperature, humidity))
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("{:d}:{:02d}:{:02d},{:g},{:g}".format(
            t.tm_hour, t.tm_min, t.tm_sec, -1, -1))

    if button.value:
        show_temperature = not show_temperature

    # Read the button
    if show_temperature:
        # Button pressed, show the temperature
        display.show(dht.temperature)
        display.show_colon = False
    else:
        # Show rotation angle
        display.show(rotary.value)
        buzzer.duty_cycle = rotary.value
        display.show_colon = True

    end = time.time()
    # Wait for the remaining time
    time.sleep(INTERVAL - (end - start))