import serial
import time



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
        print(count)
        ch_split = count.split('/')
        print(ch_split)
        ch1.append(float(ch_split[0]))
        ch2.append(float(ch_split[1]))
    return ch1, ch2




work_port = serial.Serial('COM6')
time.sleep(5)

work_port.baudrate = 115200

work_port.write(b'i')
data = read_com_data(work_port, 10)
if data == 'contactyes':
    print("OK")

work_port.write(b'm')
data = read_com_data_by_byte(work_port)
channel1, channel2 = data_parser(data)
print(channel1)
print(channel2)