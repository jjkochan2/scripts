import serial
from datetime import datetime, timezone
import argparse

parser = argparse.ArgumentParser(description="Read serial data")

parser.add_argument("--port",
                    type=str,
                    required=True,
                    help="Name of the port to listen on (try /dev/ttyUSB0)")

parser.add_argument("--baudrate",
                    type=int,
                    required=True,
                    help="Baud rate of the port")

parser.add_argument("--logfile",
                    type=str,
                    required=False,
                    default=None,
                    help="Where to log data")

parser.add_argument("--timestamp",
                    action="store_true",
                    help="Include timestamps in the log")

parser.add_argument("--no-timestamp",
                    dest="timestamp",
                    action="store_false",
                    help="Do not include timestamps in the log")

parser.set_defaults(timestamp=True)

parser.add_argument("--timeout",
                    type=float,
                    required=False,
                    default=0.050,
                    help="Timeout value for serial connection (seconds)")

parser.add_argument("--decode",
                    type=str,
                    required=False,
                    default='binary',
                    help="How you want the bytes to be decoded when outputting (ASCII, int, binary)")

args = parser.parse_args()  

ser = serial.Serial(args.port, args.baudrate, timeout=0.1)

while True:
    buffer = bytearray()
    while True:
        byte = ser.read(1)
        if byte:
            buffer.extend(byte)
        else:
            break
    if buffer:
        if args.decode == 'ASCII':
            try:
                data = buffer.decode(errors='replace').rstrip('\r\n')
            except UnicodeDecodeError:
                data = str(buffer)
        elif args.decode == 'int':
            data = ' '.join(str(byte).zfill(3) for byte in buffer)
        else:
            data = str(buffer)
        if args.timestamp:
            timestamp = f"[{datetime.now(timezone.utc).isoformat()}] "
        else:
            timestamp = ""
        log_line = f"{timestamp}{data}\n"

        # Write to file
        if args.logfile:
            with open(args.logfile, 'a') as log_file:
                log_file.write(log_line)
                log_file.flush()
        else:
            print(log_line)
