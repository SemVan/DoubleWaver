def write_file(file_name, ch1, ch2):
    if len(ch2) != len(ch2):
        print("FUCK MOTHERFUCK")

    with open(file_name, 'w') as f:
        for i in range(len(ch1)):
            row = str(ch1[i]) + '\t' +str(ch2[i])+'\r'
            f.write(row)
    return

def read_file(file_name):
    ch1 = []
    ch2 = []
    with open(file_name, 'r') as f:
        for row in f:
            row_str = row[:-1]
            row_splt = row_str.split('\t')
            ch1.append(float(row_splt[0]))
            ch2.append(float(row_splt[1]))
    return ch1, ch2


def parse_file_name(file_name):
    file_name = file_name[:-4]
    file_splt = file_name.split('_')
    name = file_splt[0]
    fp = file_splt[1]
    sp = file_splt[2]
    print(name, fp, sp)
    return name, fp, sp
