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


def send_measurement_request():


    return


def read_data():
    data = 0


    return data

get_port()