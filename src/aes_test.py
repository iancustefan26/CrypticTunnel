import random
import os
import string

session_key = ''.join(random.choice(string.printable) for x in range (30))
print(session_key)
session_key = session_key.encode('utf-8')

hex = session_key.hex()
print(hex)
