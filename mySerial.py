import serial
__author__ = 'ruggero'


class MySerial(serial.Serial):
    def myreadline(self):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            if self.inWaiting() == 0:
                break
            c = self.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)
