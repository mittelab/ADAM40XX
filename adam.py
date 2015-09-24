__author__ = 'ruggero'

class Adam(object):
    def __init__(self, model, id='00'):
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

    def send_command(self,command,**kwargs):
        """
        ......
        """
        if command in self.commands.keys():
            command = self.command_parsing(command)
        else:
            return None
        pkg_send = bytearray()
        for c in command:
            if len(c) == 1 : pkg_send.append(ord(c)); continue
            # this line MUST be improved
            if c == 'AA': pkg_send.append(int(self.__id,16))
            if c in kwargs.keys():
                pkg_send.append(int(kwargs[c],16))
        if len(pkg_send) != len(command):
            return None
        return(pkg_send)

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
    try:
        print(sens1.send_command('Enable/disable_Channels_for_Multiplexing'))
    except Exception as e:
        print(e.args[0])