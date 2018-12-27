import serial
import sys
import glob


def get_port():
    ports_list = get_list_of_com_ports()
    return find_port(ports_list)


def get_list_of_com_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        return 0

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print(result)
    return result


def find_port(port_list):
    port = serial.Serial()
    port.baudrate = 115200
    port.timeout = 1
    port.parity = serial.PARITY_NONE
    port.rtscts = 0
    for port_name in port_list:
        try:
            port.port = port_name
            port.open()
            port.write(b'i')
            s = port.read(10)
            if s != "contactyes":
                 port.close()
            else:
                return port
        except serial.SerialException as e:
            raise e
        return 0


def write_com_data(port, data):
    port.reset_input_buffer()
    port.write(bytes(data, 'utf-8'))
    return

def read_com_data(port, bytes_amount):
    while port.in_waiting == 0:
        pass

    answer = port.read(bytes_amount)
    answer_byte_list = answer.split(b'\r')
    answer_str_list = [elem.decode('utf-8') for elem in answer_byte_list]
    answer_str = ''.join(answer_str_list)
    return answer_str

def read_com_data_by_byte(work_port):
    while work_port.in_waiting == 0:
        pass

    answer = work_port.read(1)
    while answer[-1] != 13:
        while work_port.in_waiting == 0:
            pass
        answer += work_port.read(1)
    return answer


get_port()
