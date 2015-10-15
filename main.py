import serial
import adam
from time import sleep


if __name__ == '__main__':
    buffer = ''
    try:
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
    except:
        print('port fail')
        #exit(0)
    print('module >')
    module = input()
    print('Adress >')
    address = input()

    # Example:
    module = '4017'
    address = '04'

    sonda1 = adam.Adam(module, address=address)

    while True:
         c = input()
         if c == 'E':
            break
    # first question
    data, rec = sonda1.send_command('Configuration_Status_1')
    #data, rec = sonda1.send_command('Read_Analog_Input')
    print('data thet are going to be send', data)
    ser.write(data)
    # wait for answare to be collected
    sleep(1)
    # number_data = ser.inWaiting()
    dati = ser.readline()
    # dati = ser.read(number_data)
    print(dati)
    print(len(dati))
    answer = rec.receieve_command(dati)
    print(answer)
    ser.close()