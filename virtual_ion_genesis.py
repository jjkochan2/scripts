# imports
import serial
import time
import argparse

parser = argparse.ArgumentParser(description="Virtual Ion Genesis")

parser.add_argument("--port",
                    type=str,
                    required=True,
                    help="Name of the port to transmit on (try /dev/ttyUSB0)")

parser.add_argument("--baudrate",
                    type=int,
                    required=False,
                    default=19200,
                    help="Baud rate of the port (Ion Genesis is 19200)")

parser.add_argument("--wakeupbyte",
                    type=int,
                    required=False,
                    default=0xAA,
                    help="Baud rate of the port (Ion Genesis wakeup byte is 0xAA)")

args = parser.parse_args() 

def human_readable_sensor_output(data):

    # if there is data
    if data:
        # if the response passes the checksum
        if sum(data[:len(data) - 1]) % 256 == data[len(data) - 1]:
            # if the data is the correct length
            if len(data) == 9:
                water_level = 0
                for byte in data[1:4]:
                    water_level += int(byte)
                water_level /= 10
                if data[7] == 0:
                    version = '25"'
                elif data[7] == 1:
                    version = '72"'
                else:
                    version = 'Unknown'
                return f"Water Level = {water_level}\tVersion = {version}"
            else:
                return "Data incorrect length"
        else:
            return "Response failed checksum"

# functions
def request_bytes_from_sensor(number_of_bytes):

    # format the command
    send_buffer =   [
                        args.wakeupbyte,
                        number_of_bytes,
                        args.wakeupbyte + number_of_bytes
                    ]
    
    # debug
    # print(f"Ion Genesis: {bytes(send_buffer)}")
    print(f"Ion Genesis:\t{' '.join(str(byte).zfill(3) for byte in bytes(send_buffer))}")
    # debug

    # send the command
    ser.write(bytes(send_buffer))

    # wait for response
    response = ser.read(number_of_bytes + 2)

    # debug
    # print(f"Sensor: {response}")
    # formatted = ' '.join(str(byte) for byte in response)
    print(f"Sensor:\t\t{' '.join(str(byte).zfill(3) for byte in response)}")
    # print(f"        {formatted}")
    print(human_readable_sensor_output(response))

# initialize serial communication
ser = serial.Serial(args.port, args.baudrate, timeout=0.050)

# main loop
while True:
    request_bytes_from_sensor(7)
    time.sleep(0.250)
