import serial
import adam
from time import sleep


class MySerial(serial.Serial):
    def myreadline(self):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)


if __name__ == '__main__':
    buffer = ''
    try:
        ser = MySerial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )
    except serial.SerialException as Error:
        print(Error)
        print('port fail')

    print('module >')
    # module = input()
    print('Adress >')
    # address = input()

    # Example:
    module = '4017'
    address = '04'

    sonda1 = adam.Adam(module, address=address)
    debug = True



    while True:
        print('operation >')
        switch = input()

        if switch == 'help':
            print('--help--')
            print('cmd : the list of commands of the module')
            print('send: send command')
            print('info   : a lot of stuff')
            print('exit   : exit(0)')
        elif switch == 'cmd':
            print('list of available commands:')
            print(sonda1.cmd())
        elif switch == 'send':
            try:
                ser
            except NameError:
                print('serial port is not open')
                continue
            print('command to send >')
            command = input()
            data, rec = sonda1.send_command(command)
            ser.write(data)
            sleep(0.5)
            if debug:
                dati = ser.myreadline()
                print(dati, len(dati))
                answer = rec.receieve_command(dati)
                print(answer)
            else:
                print(rec.receieve_command(ser.readline()))
        elif switch == 'info':
            print(sonda1)
        elif switch == 'exit':
            try:
                ser.close()
            except NameError:
                pass
            exit(0)
        else:
            print('wrong command')