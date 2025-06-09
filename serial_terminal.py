import argparse

parser = argparse.ArgumentParser(description="Interactive Serial Terminal")

parser.add_argument("--port",
                    type=str,
                    required=True,
                    help="Name of the port to listen on (try /dev/ttyUSB0)")

parser.add_argument("--baudrate",
                    type=int,
                    required=True,
                    help="Baud rate of the port")

