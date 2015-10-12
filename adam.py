__author__ = 'ruggero'

class Adam(object):
    def __init__(self, model, address='00'):
        path = './model/%s.dat' % model
        if address[0] > 'F' or address[1] > 'F':
            raise ValueError('wrong address')
        else:
            self.__id = address
        try:
            load = open(path,'r')
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise ValueError('model not defined', 0)
        except:
             raise ValueError('No I/O error here?!?, you are fucked')
        self.commands = eval(load.read())

    def send_command(self, command, **kwargs):
        """
        ......
        """
        if command in self.commands.keys():
            command = self.command_parsing(command)
            rec = AdamReceiver(''.join(command))
        else:
            return None
        pkg_send = bytearray()
        for c in command:
            if c == 'AA':
                pkg_send += bytearray(self.__id, encoding='utf-8')
                continue
            if c in kwargs.keys():
                # this line shouldn't work
                pkg_send.append(int(kwargs.pop(c),16))
                continue
            if len(c) == 1:
                pkg_send.append(ord(c))
                continue
        # add the CR character
        pkg_send.append(13)
        return pkg_send, rec

    def command_parsing(self,command):
        cmd = self.commands[command][0]
        parse = []
        supp = []
        for i in range(len(cmd)-1):
            supp.append(cmd[i])
            if cmd[i+1] == cmd[i]:
                continue
            else:
                parse.append(''.join(supp))
                supp = []
        else:
            i += 1
            supp.append(cmd[i])
        parse.append(''.join(supp))
        return tuple(parse)


    def __str__(self):
        s = ''
        for k in self.commands.keys():
            s = s + k + ':' + str(self.commands[k][0]) + '\n' + str(self.commands[k][1]) + '\n\n'
        return s


class AdamReceiver(object):

    def __init__(self,command):
        path = './model/receive.dat'
        try:
            load = open(path,'r')
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise ValueError('receive database not found', 0)
        except:
            raise ValueError('No I/O error here?!?, you are fucked')
        commands = eval(load.read())
        self.command = self.command_parsing(commands[command])

    def receieve_command(self, received):
        if len(received) == 0:
            raise 'well, fuck'
        received = received.decode('utf-8')
        if received[0] == '?':
            return ('AA', received[1:])
        elif received[0] == '!':
            supp = []
            pointer = 0
            for i in self.command:
                supp.append(received[pointer:pointer+len(i)])
                pointer += len(i)
            xmap = zip(self.command, supp)
            return list(xmap)
        elif received[0] == ord('>'):
            print('caso 3')

    @staticmethod
    def command_parsing(command):
        parse = []
        supp = []
        flag = False
        for i in range(len(command)):
            supp.append(command[i])
            if command[i] == '(' or flag:
                flag = True
                if command[i] == ')':
                    flag = False
                    parse.append(''.join(supp))
                    supp = []
                    continue
                else:
                    continue
            if i < len(command)-1:
                if command[i+1] == command[i]:
                    continue
                else:
                    parse.append(''.join(supp))
                    supp = []
            else:
                parse.append(''.join(supp))
        return tuple(parse)

if __name__ == '__main__':
    sens1 = Adam('4017')
    a, b = sens1.send_command('Configuration_Status_1')
    #a, b = sens1.send_command('Read_Analog_Input')
    print(a)
    print(b.command)
    b.receieve_command(b'!04090680\r')
    #b.receieve_command(b'?04\r')
