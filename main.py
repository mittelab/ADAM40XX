import serial
import adam
from time import sleep
from time import time


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


def inquiring(probe, ser, t, command):
    data, rec = probe.send_command(command)
    ser.write(data)
    print(rec.receieve_command(ser.readline()))
    sleep(t)

if __name__ == '__main__':
    buffer = ''
    debug = True

    if debug:
        a1 = '/dev/ttyUSB0'
        a2 = 9600
        a3 = 8
        a4 = serial.PARITY_NONE
        a5 = serial.STOPBITS_ONE
        a6 = 0
        a7 = 0
        a8 = None
        module = '4017'
        address = '04'
    else:
        print('porta da aprire >')
        a1 = input()
        print('baudrate (9600)>')
        a2 = int(input())
        print('bytesize (8)>')
        a3 = (input())
        a4 = serial.PARITY_NONE
        a5 = serial.STOPBITS_ONE
        a6 = 0
        a7 = 0
        a8 = None
        print('module >')
        module = input()
        print('Adress >')
        address = input()

    try:
        ser = MySerial(
            port=a1,
            baudrate=a2,
            bytesize=a3,
            parity=a4,
            stopbits=a5,
            xonxoff=a6,
            rtscts=a7,
            interCharTimeout=a8
        )
    except serial.SerialException as Error:
        print(Error)
        print('port fail')

    sonda1 = adam.Adam(module, address=address)
    flag = True

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
        elif switch == 'send' and flag:
            try:
                ser
            except NameError:
                print('serial port is not open')
                continue
            print('command to send >')
            command = input()
            if debug:
                t_i = time()
            parameters = sonda1.command_parsing(command)
            if debug:
                print(time()-t_i)
            other = {}
            for c in parameters:
                if len(c) >= 2 and c != 'AA':
                    print('parametro addizionale %s >' %c)
                    other[c] = input()
            data, rec = sonda1.send_command(command, other)
            ser.write(data)
            if debug:
                sleep(0.5)
                dati = ser.myreadline()
                print(dati, len(dati))
                answer = rec.receieve_command(dati)
                print(answer)
            else:
                print(rec.receieve_command(ser.readline()))
        elif switch == 'info':
            print(sonda1)
        elif switch == 'acquisition' and flag:
            print('delay >')
            t = int(input())
            try:
                ser
            except NameError:
                print('serial port is not open')
                continue
            print('command >')
            command = input()
            inquiring(sonda1,ser,t,command)
            flag = False

        elif switch == 'stop_acq' and not flag:
            flag = True

        elif switch == 'exit':
            try:
                ser.close()
            except NameError:
                pass
            exit(0)
        else:
            print('wrong command')