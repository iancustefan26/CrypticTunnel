import ctypes

rsalib = ctypes.CDLL("rsalib.so")

public_key = rsalib.generateRSAKeyPair()

print(public_key)