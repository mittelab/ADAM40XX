__author__ = 'ruggero'


class Adam(object):
    def __init__(self, model, id=b'\x00'):
        path = './model/%s.dat' % model
        self.__id = id
        try:
            load = open(path,'r')
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise ValueError('model not defined', 0)
        except:
             raise ValueError('No I/O error here?!?, you are fucked')
        self.commands = eval(load.read())

    def send_command(self,serial,command,arg=None):
        if command in self.commands.keys():
            command = self.command_parsing(command)
        else:
            return 0
        print(command)
        return 1

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
        i = i + 1
        supp.append(cmd[i])
        parse.append(''.join(supp))
        return tuple(parse)


    def __str__(self):
        s = ''
        for k in self.commands.keys():
            s = s + k + ':' + str(self.commands[k][0]) + '\n' + str(self.commands[k][1]) + '\n\n'
        return s


if __name__ == '__main__':
    try:
        sens1 = Adam('4017')
    except Exception as e:
        print(e.args[0])
    print(sens1)
    if sens1.send_command('asdf','Enable/disable_Channels_for_Multiplexing') == True:
        print('sent')
    else:
        print('command not sent, something went wrong')