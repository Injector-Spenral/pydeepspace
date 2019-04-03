import wpilib
import time
# from hal_impl.serial_helpers import SerialSimBase


# class ColourSerialSimulator(SerialSimBase):
#     serial_string = "f0.1,0.2,0.3,0.4,0.5,0.6,0.7\nb0.9,0.2,0.3,0.4,0.5,0.6,9.8\n"

#     def readString(self, count):
#         num_strings = (count % len(self.serial_string))
#         return ([self.serial_string]*num_strings)[:count]

#     def readSerial(self, port, buffer, count, status):
#         status.value = 0
#         buffer[:] = [ord("c")] * count
#         return count


class ColourSensor:

    arduino_port: wpilib.SerialPort

    baud_rate: int = 9600
    read_char: int = 100

    num_sensors: int = 14

    reading_timeout: float = 0.4 # s

    front_char = 'f'
    back_char = 'b'

    packet_separator = '\n'
    value_separator = ','

    def __init__(self):
        self.readings = None
        self.last_reading_time = 0

    def split_packet(self, packet):
        print('splitting packet')
        try:
            packet_split = [value for value in packet.split(self.value_separator)
                            if not value == ""]
            # todo - exclude empty strings here
            reading = [
                float(reading)
                for reading in packet_split
            ]
            print(f'reading raw {reading}')
            if len(reading) == self.num_sensors:
                return reading
        except ValueError:
            pass
        print('returning none')
        return None

    def execute(self):
        # total_str = ""
        total_str = self.arduino_port.readString(count=self.read_char)
        print(f"Total str {total_str}")
        packets = total_str.split(self.packet_separator)
        print(f"Packets {packets}")

        # parse out the front and back
        for packet in reversed(packets):
            print(f'Parsing {packet}')
            if packet == "":
                continue
            values = self.split_packet(packet)
            if values is not None:
                self.last_reading_time = time.monotonic()
                self.front_r
        if (time.monotonic() - self.last_reading_time) > self.reading_timeout:
            self.readings = None
        print(f'readings {self.readings}')
