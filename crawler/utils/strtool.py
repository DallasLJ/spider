#!/usr/bin/python3

def find_last_index(str, sep):
    times = len(str) - len(sep)
    length = len(sep)
    index = -1
    for i in range(times+1):
        if str[i: i + length] == sep:
            index = i
    return index

if __name__ == '__main__':
    print(find_last_index('http://www.baidu.com/s', '/'))
