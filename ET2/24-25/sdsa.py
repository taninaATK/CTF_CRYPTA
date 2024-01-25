from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import secrets
import hashlib
from pyasn1.type import univ
from pyasn1.codec.der.encoder import encode as der_encode
from pyasn1.codec.der.decoder import decode as der_decode


print("SDSA : ")

public_key_dsa = b"""-----BEGIN PUBLIC KEY-----
MIIDSDCCAjoGByqGSM44BAEwggItAoIBAQD+TrmX70MlK5VQTB/3ByHaipCp6N5C
QKT5+WOXcPIgXU0+f3rdj6TvflvYZOaaQj53oVQDOg4FEbc8y7mfYz7LoAGFbXnv
ylxjbRjLAvCnw4NfqaFPuOLjV+k948OkjcnqGkeNG6+XSxDZgNjXYs+55+PD7nsX
ARLdwL/k7hKfY8bt2bLw77GX+A6LBIOCzxPqdV1vSwO5tFiLBjXyjo26A00RuKI1
xX4Be+nSdt8U+2dCs55Tzvq1Zm10CKCMCiJ4BFObgHP6G7JVuXHwsxbyhHWaF0a4
01e1ITsJeI1lDoYGkrFlNSQCUdxeo1Gkz2N+3JQm0cPlgRDmJXHiSDjNAiEA7/BY
XCmA8Ng8RKfqXZh/Ds0BeDYPI3Bhgs0wpIbOqYsCggEBAJcQdO866MgpH9yOI09s
yAKqTA5K3Qv5hyGJVq1QasYYabHvdI4zCmCrro2evIrU5FMAiBLMeSnlA0QCGhD7
EkU92GN/gfJ7bYSkTxEN/KCT1nlcBJpWyRDZBcbBJmKGZjPo0QIDQ+Y9JjJsGclk
9ZtjGVrXLDq3g/QQU304KXxiFs7GyC+0sunCLDMfjXY8vsOwAC0MgNenGdsIT2io
iRRTFXnVne47EMVt9y8MswMl1Sv9aKyGjYhN47a9z2uZC4y4RVVU1s/vymLG424G
W6Y7z5mDO33HdO/Rr+yCYjbX+2Vn1MHpNfO5gfFzu6ya7lbKM936JdgCKXTMFpIK
Z6sDggEGAAKCAQEAuGsuam12bfD0lOA7bhzmvLUUZC5EB//x/hYxCm/GCyyPP0FC
PylUWxWUuB9DU2CNsvF7LIIKQse/z+05ultj3+8wlIDHQlSZhJ/t3A8wGW7wRUJp
NuDP/9SptQ6dzIqtMRehtawJ3n5TkxqRZZT5THPvMUmNgNywEOVccxxPig9QUHbt
D3taOhlzZOfdDQm8XX5lD+3yfOrC8lTJiGCJ7W5MzrE4DElWsBoUqBMwxVsfk35L
no2PiImK2F5jBL6pC/hsxvLLKVr29JqYZCYSHUkcJTub4Gsl5UAkc87i040GtFP7
hnDNSKl7k59+i6P3JYhMJr52Lbkp5Gpilhwo6w==
-----END PUBLIC KEY-----"""

# 2 signatures using the same k
sig_1 = "30460221008E9B2087B902946C05C8E9002E207D7B138D21FDD472990AE894286E1CC39F4E022100D2F5597684DAE80C9A7394055B2CDACFBC621E78A445FC16FF3F4F006D45CCDE"
sig_2 = "30430220074816B8560E59D573BB1CE28C16ABB1D46473F2BAA80E80433389D9F51B5E8B021F1793E2DB61639275C15411D11AA21B5FEADA7C5F50EDB4B52BAF46FA0378C7"

challenge = input("Input the challenge : ")
public_key = serialization.load_pem_public_key(
    public_key_dsa,
    backend=default_backend()
)

if public_key.key_size is None or public_key.public_numbers().parameter_numbers is None:
    print("Not a DSA public key :(")
    exit(1)

p = public_key.public_numbers().parameter_numbers.p
q = public_key.public_numbers().parameter_numbers.q
g = public_key.public_numbers().parameter_numbers.g

print("YOUR PUBLIC KEY VARIABLES : ")
print(f"p: {p}")
print(f"q: {q}")
print(f"g: {g}")

# first decode the signature : get c1 and s1
signature_der = bytes.fromhex(sig_1)
# decode from DER to ASN.1 structure
signature_asn1, remainder = der_decode(signature_der, asn1Spec=univ.Sequence())
# extract c and s from the ASN.1 structure
c1 = int(signature_asn1.getComponentByPosition(0))
s1 = int(signature_asn1.getComponentByPosition(1))

# then get c2 and s2
signature_der = bytes.fromhex(sig_2)
# decode from DER to ASN.1 structure
signature_asn1, remainder = der_decode(signature_der, asn1Spec=univ.Sequence())
# extract c and s from the ASN.1 structure
c2 = int(signature_asn1.getComponentByPosition(0))
s2 = int(signature_asn1.getComponentByPosition(1))
print(f"c1 : {c1}")
# we have s = k + c * x mod q use it with s1, s2, c1, c2 to find x and k
x = ((s1 - s2) * pow(c1 - c2, -1, q)) % q
# then put x in and find k
k = (s1 - c1 * x) % q

# now that you have all this, nice, you can replicate the signature process
# use r = g**k mod p.
r = pow(g, k, p)

# r to byte rep
r_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
message = challenge.encode() + r_bytes

# compute the hash of message
final_hash = hashlib.sha256(message).digest()
n = q.bit_length()
# big -> most significant byte is at the beginning
z = int.from_bytes(final_hash, 'big')
# IF YOU ENCOUNTER ISSUES USE THIS
# mask so that it's masked beyond n (but not really necessary)
# z = z & ((1 << n) - 1) # (chatgpt gave me this one lol)
c = z % q
# s = k + c * x mod q.
s = (k + c * x) % q
# create ASN.1
signature_asn1 = univ.Sequence()
signature_asn1.setComponentByPosition(0, univ.Integer(c))
signature_asn1.setComponentByPosition(1, univ.Integer(s))
# der
signature_der = der_encode(signature_asn1)
# hex
signature_hex = signature_der.hex()
print(f"Final signature : {signature_hex}")

# verify the signature : r <-- g**s * h**(-c) modulo p
h = pow(g, x, p)
r = (pow(g, s, p) * pow(h, -c, p)) % p
signature_der = bytes.fromhex(signature_hex)
signature_asn1, remainder = der_decode(signature_der, asn1Spec=univ.Sequence())
c_verif = int(signature_asn1.getComponentByPosition(0))
s_verif = int(signature_asn1.getComponentByPosition(1))

# message = challenge + hex(r)
# hash_object = hashlib.sha256(message.encode())
# c_final = int(hash_object.hexdigest(), 16)
r_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
message = challenge.encode() + r_bytes
# compute the hash of message
final_hash = hashlib.sha256(message).digest()
n = q.bit_length()
z = int.from_bytes(final_hash, 'big')
# z = z & ((1 << n) - 1)
c_final = z % q
if (c_verif == c_final):
	print("YES")
else:
	print("NO")
