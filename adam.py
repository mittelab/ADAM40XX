import re
__author__ = 'ruggero'

class Adam(object):
    def __init__(self, model, address='00'):
        path = './model/%s.dat' % model
        self.__model = model
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
        this method given a command and the list of parameters needed return a bytearray and a reciver class
        """
        # primary check
        if command in self.commands.keys():
            command = self.command_parsing(command)
            #rec = AdamReceiver(''.join(command))
        else:
            raise ValueError('command not defined')

        # build the command
        pkg_send = bytearray()
        for c in command:
            if c == 'AA':
                pkg_send += bytearray(self.__id, encoding='utf-8')
            elif c in kwargs.keys() or c == 'N':
                pkg_send += bytearray(kwargs.pop(c), encoding='utf-8')
                # pkg_send.append(int(other.pop(c),16))

            elif len(c) == 1:
                pkg_send.append(ord(c))
            else:
                raise ValueError('error in the parameters')
        # add the CR character
        pkg_send.append(13)

        # creation of the receiver function
        def rec(received):
            debug = False
            nonlocal command
            path = './model/receive.dat'
            try:
                load = open(path,'r')
            except IOError as e:
                print ("I/O error({0}): {1}".format(e.errno, e.strerror))
                raise ValueError('receive database not found')
            except:
                raise ValueError('No I/O error here?!?, you are fucked')

            # answer database parsing here
            commands = eval(load.read())

            # if there is a standard answer, do the parsing
            if command in commands:
                rec_command = []
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
                            rec_command.append(''.join(supp))
                            supp = []
                    else:
                        rec_command.append(''.join(supp))
                rec_command = tuple(rec_command)
            else:
                rec_command = None

            # Decoding starts here
            if len(received) == 0:
                return [('data', None),('error', '0 data received')]

            received = received.decode('utf-8')

            if received[0] == '?':
                # wrong command has been sent
                return [('AA', received[1:-1]), ('error', 'wrong command has been sent')]
            elif received[0] == '!':
                # commando with info has been sent
                if rec_command is None:
                    return [('info', received[1:])]
                else:
                    supp = []
                    pointer = 0
                    for i in rec_command:
                        supp.append(received[pointer:pointer+len(i)])
                        pointer += len(i)
                    xmap = zip(rec_command, supp)
                    if debug: print(list(xmap))
                    return list(xmap)
            elif received[0] == '>':
                # command with data has been sent
                l1=[]
                l = re.findall(r'([-+]\d+.\d+)', received[1:])
                for i in range(len(l)):
                    s = 'IN' + str(i)
                    l1.append((s, l[i]))
                if debug: print(l1)
                return l1
            else:
                return [('data', None),('error', 'not standard pack')]

        return rec

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

    def cmd(self):
        s = ''
        for k in self.commands.keys():
            s = s + k + ':' + str(self.commands[k][0]) + '\n'
        return s

    def __str__(self):
        s = 'initialized module = ' + str(self.__model) + '\n'
        s = s + 'initialized address = ' + str(self.__id) + '\n\n'
        for k in self.commands.keys():
            s = s + k + ':' + str(self.commands[k][0]) + '\n' + str(self.commands[k][1]) + '\n\n'
        return s




if __name__ == '__main__':
    sens1 = Adam('4017')
    a = sens1.send_command('ConfB')
    #print(a)
    #print(b.command)
    print('-----')
    print(a(b'!04090680\r'))
    print('----')
    print(a(b'?04\r'))
    print('----')
    a = sens1.send_command('ReadAll')
    print(a(b'>+0.5-0.4+9.2-7.5\r'))
