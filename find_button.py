import RPi.GPIO as GPIO
import time

starting_state = []
ending_state = []
death_pins = [28, 29]

for PIN in range(30):
    if PIN not in death_pins:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        state = GPIO.input(PIN)
        print(f"Pin: {PIN} State: {state}")
        starting_state.append(state)

input("Press enter while holding button.")

for PIN in range(30):
    if PIN not in death_pins:
        state = GPIO.input(PIN)
        print(f"Pin: {PIN} State: {state}")
        ending_state.append(state)

button_found = False
for index in range(len(max(starting_state, ending_state))):
    if starting_state[index] != ending_state[index]:
        print(f"Button is on PIN {index}")
        button_found = True
if not button_found:
    print("Button not found :(")
