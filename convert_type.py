from ctypes import *


def convert_type(input):
    ctypes_map = {int: c_int,
                  float: c_float,
                  str: c_char_p
                  }
    input_type = type(input)
    if input_type is list:
        length = len(input)
        if length == 0:
            print("convert type failed...input is " + input)
            return None
        else:
            arr = (ctypes_map[type(input[0])] * length)()
            for i in range(length):
                arr[i] = bytes(input[i], encoding="utf-8") if (type(input[0]) is str) else input[i]
            return arr
    else:
        if input_type in ctypes_map:
            return ctypes_map[input_type](bytes(input, encoding="utf-8") if type(input) is str else input)
        else:
            print("convert type failed...input is " + input)
            return None