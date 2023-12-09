from ctypes import *
import numpy as np
import numpy.ctypeslib as npct


def lib_init(dll_root='./ElectronBotSDK-LowLevel.dll'):
    lib = CDLL(dll_root)

    class OBJ(Structure):
        _fields_ = []

    ARRAY = npct.ndpointer(dtype=np.uint8, shape=(240, 240, 3))

    lib.CreateElectronLowLevel.restype = POINTER(OBJ)
    lib.mySetImageSrc.argtypes = POINTER(OBJ), ARRAY,
    lib.mySetJointAngles.argtypes = POINTER(OBJ), POINTER(c_float), c_int
    lib.myGetJointAngles.restype = POINTER(c_float)  # 读取之前必须关闭使能

    return lib
