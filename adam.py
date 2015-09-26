__author__ = 'ruggero'

class Adam(object):
    def __init__(self, model, adress='00'):
        path = './model/%s.dat' % model
        self.__id = adress
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
        else:
            return None
        pkg_send = bytearray()
        for c in command:
            if c == 'AA':
                pkg_send.append(int(self.__id,16))
                continue
            if c in kwargs.keys():
                pkg_send.append(int(kwargs.pop(c),16))
                continue
            if len(c) == 1:
                pkg_send.append(ord(c))
                continue
        if len(pkg_send) != len(command):
            return None
        # add the CR character
        pkg_send.append(13)
        return pkg_send

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
        self.command = commands[command]


if __name__ == '__main__':

    try:
        sens1 = Adam('4017')
    except Exception as e:
        print(e.args[0])
    try:
        print(sens1.send_command('Read_Analog_Input', N='2'))
    except Exception as e:
        print(e.args[0])