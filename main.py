from mySerial import MySerial
import serial
import adam
import RepeatedTimer
from time import sleep
import csv


if __name__ == '__main__':
    buffer = ''
    debug = True
    while True:
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
            a3 = int(input())
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
            break
        except serial.SerialException as Error:
            print(Error)
            print('port fail')
            if debug:
                break

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
            parameters = sonda1.command_parsing(command)
            other = {}
            for c in parameters:
                if (len(c) >= 2 and c != 'AA') or c =='N':
                    print('parametro addizionale %s >' %c)
                    other[c] = input()
            data, rec = sonda1.send_command(command, **other)
            ser.write(data)
            if debug:
                sleep(0.5)
                dati = ser.myreadline()
                print(dati, len(dati))
                answer = rec(dati)
                print(answer)
            else:
                print(rec(ser.myreadline()))

        elif switch == 'info':
            print(sonda1)

        elif switch == 'acq' and flag:
            print('delay >')
            t = int(input())
            print('file name >')
            file = input()
            try:
                ser
            except NameError:
                print('serial port is not open')
                continue
            file = open(file, 'a')
            w = csv.writer(file, dialect='excel')
            c.writerow(["time", "Address"])
            print('command >')
            command = input()
            parameters = sonda1.command_parsing(command)
            other = {}
            for c in parameters:
                if (len(c) >= 2 and c != 'AA') or c =='N':
                    print('optional parameter {} >'.formtat(c))
                    other[c] = input()
            command, receiver = sonda1.send_command(command, **other)
            ser.write(command)
            data = receiver(ser.my_read_line())
            c.writerow(data)
            process = RepeatedTimer.RepeatedTimer(t, ser.inquiring, command, receiver, w)
            process.start()
            flag = False
            print('process is starting')

        elif switch == 'stop_acq' and not flag:
            file.close()
            process.stop()
            flag = True
            print('process has been stopped')

        elif switch == 'exit':
            try:
                ser.close()
            except NameError:
                pass
            exit(0)
        elif not flag:
            print('port busy')
        else:
            print('wrong command')