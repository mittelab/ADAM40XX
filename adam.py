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
            self.command_parsing(command)
        else:
            return 0
        return 1

    def command_parsing(self,command):
        cmd = self.commands[command][0]
        print(len(cmd))

    def __str__(self):
        s = ''
        for k in self.commands.keys():
            s = s + k + ' '
        return s


if __name__ == '__main__':
    try:
        sens1 = Adam('4017')
    except Exception as e:
        print(e.args[0])
    print(sens1)
    if sens1.send_command('asdf','Configuration') == True:
        print('sent')
    else
        print('command not sent, something went wrong')