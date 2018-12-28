import serial



def get_list_of_com_ports():
    ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def find_port(port_list):
    work_port = serial.Serial()
    work_port.baudrate = 115200
    work_port.timeout = 10
    work_port.write_timeout = 3
    work_port.parity = serial.PARITY_NONE
    work_port.bytesize = serial.EIGHTBITS
    work_port.rtscts = True
    for port in port_list:
        print("Scanning port {ort}".format(ort=port))
        work_port.port = port
        work_port.close()
        work_port.open()
        try:
            work_port.write(b'i\r')
        except serial.SerialTimeoutException:
            continue
        answer = read_com_data(work_port, 10)

        if answer == "contactyes":
            print("Port found")
            return work_port
        else:
            work_port.close
    return 1


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

    answer = work_port.read(3)
    while answer[-3:] != b'end':
        while work_port.in_waiting == 0:
            pass
        answer += work_port.read()
    return answer

def data_parser(data):
    data_str = data.decode( 'utf-8')
    data_str = data_str[:-4]
    count_splt = data_str.split('|')
    ch1 = []
    ch2 = []
    for count in count_splt:
        ch_split = count.split('/')
        ch1.append(float(ch_split[0]))
        ch2.append(float(ch_split[1]))
    return ch1, ch2


def one_measurement_procedure(port):
    port.write(b'm')
    data = read_com_data_by_byte(port)
    channel1, channel2 = data_parser(data)
    return channel1, channel2

