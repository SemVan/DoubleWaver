def write_file(file_name, ch1, ch2):
    if len(ch2) != len(ch2):
        print("FUCK MOTHERFUCK")

    with open(file_name, 'w') as f:
        for i in range(len(ch1)):
            row = str(ch1[i]) + '\t' +str(ch2[i])+'\r'
            f.write(row)
    return
