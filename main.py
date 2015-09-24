import serial
import array
from time import sleep


if __name__ ==  '__main__':
    buffer = ''
    ser = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        bytesize=8,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.25,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None
    )
    s = 'test'
    s_conv = bytearray()
    s_conv.extend(map(ord, s))
    s_conv = hex(0xFF)
    print (s_conv)

    while True:
        #ser.write(s.encode(encoding='utf-8'))
        ser.write(b'\x6F\xff')
        #s.encode  ascii()
        sleep(0.1)
        #print(ser.read(6))
        print(ser.read(ser.inWaiting()))
        #print(ser.read(ser.inWaiting())

    ser.close()