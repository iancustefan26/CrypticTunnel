import rsalib
import time
import os

#public_key, private_key = rsalib.generateRSAKeyPair()

plaintext = "Salut, sunt Stefan"
private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAmiInDr6TBfPkGfzoM0/JL5DuT/dn8Z83oDSCwZuMdXwyanBu
ryPuDsuP5doB+Xez2Ioa4ebIjvfBqylEt4F+5VDclY8bj07NJypDuCp+9AfXmhPg
cfu91pwitvYpC+BrwyEDY4z8sVgx/+Eq5AUeRNj/HzUUGbgvAQEKN0r3pVJiyg/5
CtIAz8nSymABvmWRYKFSFEBH47yN2AvpXc4DT0+DXUKEwbAn6LZZ23jzGWaDehGy
cW69+zI0vG7Bk9uZqiKLpgjWNZH4uS0zhQInr+N9OuxW7U7M15hFMEGkFu1Vo4Bm
/NPTgYufvwWPMcuafYJtziEtMpSlSVNzvxpeuQIDAQABAoIBAAixEQIcLbmciuoK
606BcEyWCqpIaackHa8+EXrjek83EAy/3FiqA7Gijwcc0mxZRgiu+QcbdtyBDNMf
F6NAJ9dnRkPKIc66AzLzMjBqImXrz0pUAUh23roBwf9j8DqdjtYeaszWqs/sCPMZ
+nYzR7AFi0Ac7njo0asSfkX8nJceRiY3bnEDN8C+1KMQv5d+ZNFw7XBCoaXVk2Yu
tdHbn3ebKW3UdCiA8ecISokKxOiOFZCLwcdEdRHslyisVpxMVouzrZqlGks5DMTC
X8e8XPI3ODiHixwEsEVNkuPOEytyd3w3Oyvf86pfNvJ+CwYMHuK3KhyF6EyC5o+L
JBMTYnUCgYEAyQy9dhgutbALIRgorIjhx9rZRyLCJ1b5gFXM7n7ea/Sd+o754nIM
CV4eHIeFfv4UnsJb7CO5mc5WugTkg986zDRbzUCVmIa6UtGUx/y2k9CGEMt7Qj3N
rb/lx5lzrtMzaEUYxbwXuRnL13aubXL83Q4Q/YFub4iyEncIdAO/2csCgYEAxEK4
RSySStONpbg3SY4LEthYnkSudgsYcmf8KDQblBUr+pJB8E/69MXgbRQKIacPzR8/
NSJltgg2ucfmSBkklrAEZW5Kd9MMBFs+bHLJ1VDjM1PpW+0B3/zmf812FDE1yYgl
9TloHC8SPPQ/MqQa/PexwbDWtFo12sM2c76fqQsCgYEAnjr7pcUUhgP+TlaQNHIq
mDtCg/z0JzgJd5qPhiitbvN/niIGwtSVao37TuLOCwt3OReoduoK+eTuVsrg+nSm
9u5CTgEFe5yVafbujJL1MtKLoQ40fQbdKGD+PCAmbrJkJC01ePI3DYQi7PnH//Xe
0y9t6caDHx7LX0L1kTEePg8CgYBVQsL40jcvqJ41q0ThgILRCgndn+rGv2U8dm42
LQT6HQSBE77vnl9grQIlgPoxynjz3KpB9BKJtSHJLc2d7sZVbFxMkFBro9Tpo5YH
2QpT0JMTflW3qMwSubSNOv4cIZDDX5FV6j2PWOescVNvNZm/4f9oLOHpcfNJeVsT
h3GnJwKBgFjgUeb+yOt3P9rlzHKbtyMhFUNEg32q6SC0v8R7mPIMRvifF7XF6Exd
R/CFOCQFDrmS2L/FslQBatCR/tDOuRnFddUWkjl5crQc7HgoBhajPs9lw/Dj16Uh
BjDXVD9PQR2y6OxHdgWXgf6McGO0k8R27wPI3M56sQV06rWTtmNO
-----END RSA PRIVATE KEY-----"""""


with open("temp.bin", "rb") as f:
    data = f.read(1024)

#printable_data = ''.join([chr(byte) for byte in data])

#print(printable_data)

decrypted_plain = rsalib.rsa_decrypt(private_key)

#os.remove(out_file)

print(decrypted_plain)


