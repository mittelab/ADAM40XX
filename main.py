import serial
import adam
from time import sleep


if __name__ ==  '__main__':
    buffer = ''
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=8,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None
    )
    sonda1 = adam.Adam('4017', adress='00')
    for i in range(1):
        data = sonda1.send_command('Configuration_Status_1')
        print(data)
        ser.write(data)
        sleep(1.5)
        print(ser.read(10))

    ser.close()