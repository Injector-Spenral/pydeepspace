import wpilib


class ColourSensor:

    arduino_port: wpilib.SerialPort

    baud_rate: int = 9600
    read_char: int = 100

    num_sensors: int = 7

    front_char = 'f'
    back_char = 'b'

    packet_separator = '\n'
    value_separator = ','

    def __init__(self):
        self.front_readings = None
        self.back_readings = None

    def split_packet(self, packet):
        return [
            float(reading)
            for reading in packet.split(self.value_separator)
        ]

    def execute(self):
        total_str = ""
        while True:
            read_str = self.arduino_port.readString(count=self.read_char)
            if read_str:
                total_str += read_str
            if not read_str or len(read_str) < self.read_char:
                break
        packets = total_str.split(self.packet_separator)

        # if we don't at least have one reading for each sensor, presume
        # something has gone wrong...
        if not len_packets > 1:
            self.front_readings = None
            self.back_readings = None

        # parse out the front and back
        front = None
        back = None
        for packet in reversed(readings):
            lead_char = packet[0]
            if lead_char not in [self.front_char, self.back_char]:
                # packet badly formed
                continue
            elif lead_char == self.front_char and front is None:
                try:
                    front = self.split_packet(packet)
                except ValueError: # can't read one of the floats
                    continue
            elif lead_char == self.back_char and back is None:
                try:
                    back = self.split_packet(packet)
                except ValueError: # can't read one of the floats
                    continue
            if front and back:
                self.front_readings = front
                self.back_readings = back
                break
        if front is None or back is None:
            self.front_readings = None
            self.back_readings = None
