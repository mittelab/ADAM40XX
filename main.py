from mySerial import MySerial
import serial
import adam
import RepeatedTimer
from time import sleep
import csv


if __name__ == '__main__':
    buffer = ''
    debug = False
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
            print('Lista delle porte disponibili:')
            ls = MySerial.serial_ports()
            if len(ls) == 0:
                print('Nessuna porta seriale disponibile.')
                exit(0)
            for i in range(len(ls)):
                print('{}, porta = {}'.format(i,ls[i]))
            print('# porta da aprire >')
            while True:
                try:
                    a1 = int(input())
                    if a1 > len(ls):
                        raise NameError
                    a1 = ls[a1]
                    break
                except NameError:
                    print('valore errato')

            print('inserire il valore del baudrate (tipico 9600)>')
            while True:
                try:
                    a2 = int(input())
                    break
                except NameError:
                    print('valore errato')

            print('inserire il valore del bytesize (tipico 8)>')
            while True:
                try:
                    a3 = int(input())
                    break
                except NameError:
                    print('valore errato')
            # other default parameter not implemented
            a4 = serial.PARITY_NONE
            a5 = serial.STOPBITS_ONE
            a6 = 0
            a7 = 0
            a8 = None
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
    while True:
        print('inserire il nome del modulo da inizializzare >')
        module = input()
        print('inserire l\'indirizzo del modulo da inizializzare >')
        address = input()
        try:
            sonda1 = adam.Adam(module, address=address)
            break
        except ValueError as e:
            print(e)

    # this flag is false if a background operation on the serial
    # port is active
    flag = True

    while True:
        print('operazione richiesta >')
        switch = input()

        if switch == 'help':
            print('--help--')
            print('send: spedire un comando')
            print('acq: iniziare una sessione di acquisizione')
            print('stop: terminare una sessione di acquisizione')
            print('cmd : lista dei comandi disponibili nel modulo')
            print('info: un sacco di informazioni sui comandi disponibili')
            print('exit: uscire dal programma')

        elif switch == 'send' and flag:
            print('comando da spedire >')
            command = input()
            parameters = sonda1.command_parsing(command)
            other = {}
            for c in parameters:
                if (len(c) >= 2 and c != 'AA') or c =='N':
                    print('parametro addizionale {} >'.format(c))
                    other[c] = input()
            data, rec = sonda1.send_command(command, **other)
            ser.write(data)
            if debug:
                sleep(1)
                dati = ser.my_read_line()
                print(dati, len(dati))
                print(rec(dati))
            else:
                print(rec(ser.my_read_line()))

        elif switch == 'acq' and flag:
            print('delay >')
            t = int(input())
            print('nome del file>')
            file = input()
            file += '.xls'
            print('comando da spedire >')
            command = input()
            parameters = sonda1.command_parsing(command)
            if parameters[0] != '#':
                print('comando non valido ai fini di acquisizione')
                continue
            file = open(file, 'a')
            w = csv.writer(file, dialect='excel')
            w.writerow(["delay", "Address"])
            w.writerow([t, sonda1.get_id()])
            other = {}
            for c in parameters:
                if (len(c) >= 2 and c != 'AA') or c == 'N':
                    print('optional parameter {} >'.format(c))
                    other[c] = input()
            command, receiver = sonda1.send_command(command, **other)
            ser.write(command)
            sleep(2)
            data = receiver(ser.my_read_line())
            print(data)
            w.writerow([i[0] for i in data])
            w.writerow([i[1] for i in data])
            process = RepeatedTimer.RepeatedTimer(t, ser.inquiring, command, receiver, w)
            process.start()
            flag = False
            print('processo di acquisizione iniziato.\nPrima di eseguire altre '
                  'operazioni sulla porta seriale è necessario bloccare l\' acquisizione')

        elif switch == 'stop' and not flag:
            process.stop()
            file.close()
            flag = True
            print('Il processo è stato fermato')

        elif switch == 'cmd':
            print('lista dei comandi disponibili:')
            print(sonda1.cmd())

        elif switch == 'info':
            print(sonda1)

        elif switch == 'exit':
            if not flag:
                process.stop()
                file.close()
            try:
                ser.close()
            except NameError:
                pass
            exit(0)

        else:
            print('comando non supportato o acquisizione in corso')
