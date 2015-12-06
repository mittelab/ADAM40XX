import serial
__author__ = 'ruggero'


class MySerial(serial.Serial):
    def my_read_line(self):
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

    def inquiring(self, command, rec):
        self.write(command)
        print(str(rec(self.my_readl_ine())))
        #scrivere