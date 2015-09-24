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
        timeout=0.25,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None
    )
    sonda1= adam.Adam('4017')
    for i in range(5):
        data = sonda1.send_command('Enable/disable_Channels_for_Multiplexing')
        ser.write(data)
        sleep(0.1)
        print(ser.read(6))

    ser.close()