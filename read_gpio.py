import RPi.GPIO as GPIO
import time
from datetime import datetime, timezone
import argparse

parser = argparse.ArgumentParser(description="Read gpio data")

def high_low_to_int(value):
    value_upper = value.upper()
    if value_upper == "HIGH":
        return GPIO.HIGH
    elif value_upper == "LOW":
        return GPIO.LOW
    else:
        raise argparse.ArgumentTypeError("Value must be 'HIGH' or 'LOW'")

parser.add_argument("--logfile",
                    type=str,
                    required=False,
                    default=None,
                    help="Where to log data")

parser.add_argument("--pin",
                    type=int,
                    required=True,
                    help="Which pin you want to track the state of")

parser.add_argument("--timestamp",
                    action="store_true",
                    help="Include timestamps in the log")

parser.add_argument("--no-timestamp",
                    dest="timestamp",
                    action="store_false",
                    help="Do not include timestamps in the log")

parser.set_defaults(timestamp=True)

parser.add_argument("--alarm-pin",
                    type=int,
                    required=False,
                    default=None,
                    help="Which pin you want to set when your alarm criteria is reached")

parser.add_argument("--alarm-pin-on-logic",
                    type=high_low_to_int,
                    required=False,
                    default="LOW",
                    help="Pin state: 'HIGH' or 'LOW'")


args = parser.parse_args()

# print(f"alarm_pin: {args.alarm_pin}")

GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
if args.alarm_pin:
    GPIO.setup(args.alarm_pin, GPIO.OUT)
    if args.alarm_pin_on_logic == GPIO.HIGH:
        GPIO.output(args.alarm_pin, GPIO.LOW)
    elif args.alarm_pin_on_logic == GPIO.LOW:
        GPIO.output(args.alarm_pin, GPIO.HIGH)
    else:
        raise RuntimeError("Invalid alarm_pin_on_logic input.")

    alarm_pin_state = GPIO.input(args.alarm_pin)
prev_state = GPIO.input(args.pin)

while True:
    state = GPIO.input(args.pin)
    if state != prev_state:
        if args.timestamp:
            timestamp = f"[{datetime.now(timezone.utc).isoformat()}] "
        else:
            timestamp = ""
        line = f"{timestamp}{state}\n"
        if args.logfile:
            with open(args.logfile, 'a') as log_file:
                log_file.write(line)
                log_file.flush()
        else:
            print(line)
        if args.alarm_pin:
            if GPIO.input(args.alarm_pin) != args.alarm_pin_on_logic:
                GPIO.output(args.alarm_pin, args.alarm_pin_on_logic)
                print(f'Pin {args.alarm_pin} set to {args.alarm_pin_on_logic}')
        
    prev_state = state
    time.sleep(0.010)
