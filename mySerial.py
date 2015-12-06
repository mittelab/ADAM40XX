import serial
__author__ = 'ruggero'


class MySerial(serial.Serial):
    def my_read_line(self, eol=b'\r'):
        """
        this function read binary data from the serial
        port up to an eol character or no more character on the line
        it is a blocking function.
        :return:
        return all the characters in binary form
        """
        len_eol = len(eol)
        line = bytearray()
        while True:
            if self.inWaiting() == 0:
                break
            c = self.read(1)
            if c:
                line += c
                if line[-len_eol:] == eol:
                    break
            else:
                break
        return bytes(line)

    def inquiring(self, command, rec, save):
        """
        this function inquire the serial port with a specific command,
        wait for the result, and save it in to a csv file.
        It is useful if it run on a different thread.
        :param command:
        command to send
        :param rec:
        function to parse the received data
        :param save:
        csv writer for saving purpose
        :return:
        None
        """
        self.write(command)
        data = rec(self.my_read_line())
        print(str(data))
        data = [i[1] for i in data]
        save.writerow(data)
        return None
