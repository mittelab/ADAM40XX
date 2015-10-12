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
    sonda1 = adam.Adam('4017', address='04')
    for i in range(1):
        data, rec = sonda1.send_command('Configuration_Status_1')
        #data, rec = sonda1.send_command('Read_Analog_Input')
        print(data)
        ser.write(data)
        sleep(1)
        number_data = ser.inWaiting()
        dati = ser.read(number_data)
        print(dati)
        print(len(dati))
        rec.receieve_command(dati)

    ser.close()