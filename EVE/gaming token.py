'''
Pair : 73fa0f02dee65327570e6caa2d457fa69c23fc26bb439e78b48adf73f014b2e7
Signature : 303502183527A7A76623163BFB6D4FAFF7D2A2AB54972B6C1A784734021900C2E20666A5D013FA92BCE9B308D0DE4785CA7D72F6B0299B
'''

from os import urandom
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def generate(A, K, X, Y) :
    A.append(urandom(16))
    #A.append(bytes.fromhex('00112233445566778899aabbccddeeff'))
    A.append(A[0])
    
    for i in range(1, 1024) :
        to_add = hashlib.sha256(A[i]).digest()
        A.append(to_add[:16])
        A.append(to_add[16:])
        
    for i in range(0, 1024) :
        K.append(A[i + 1024])
        aes_cipher = AES.new(K[i], AES.MODE_ECB)
        X.append((aes_cipher.encrypt(pad(bytes.fromhex('00000000000000000000000000000000'), AES.block_size)))[:16])
        Y.append((aes_cipher.encrypt(pad(bytes.fromhex('ffffffffffffffffffffffffffffffff'), AES.block_size)))[:16])
 
    print(A[2].hex())
    print(K[0].hex())
    print(X[0].hex())
    print(Y[0].hex())
    

#########################################################################################################
#########################################################################################################
#########################################################################################################

A = []
K = []
X = []
Y = []
C =''

generate(A, K, X, Y)

for i in range(1024) :
    C += (X[i].hex() + Y[i].hex())
    
C = hashlib.sha256(bytes.fromhex(C)).digest()

print("Commitment : ", C.hex())

challenge = int(input("Entrez le challenge :"))
print()

print("X[i] + Y[i]", (X[challenge]).hex()+(Y[challenge]).hex())
print()

j = challenge + 1024    
path = []

for k in range(10) :
    path.append(A[j ^ 1])
    j = j//2
    
print("Path : ")
for p in path :
    print(p.hex())