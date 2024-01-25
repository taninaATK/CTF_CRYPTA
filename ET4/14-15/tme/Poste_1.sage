from sage.modules.free_module_integer import IntegerLattice

n = 7
a = 0x25d2b7401d8e46f0
p = 0x4b54396fcce69e06
L = 2**54.76

m = matrix(n)
m[0, 0] = 1


#Initialisation de la matrice
for i in range(1, n) :
    m[i, i] = p
    m[0, i] = (a ** i) % p

#print(m)
mlll = IntegerLattice(m);
#print(mlll)
v = mlll.shortest_vector(algorithm="fplll")

#Making sure it is correct
print(v)
print(v.norm().n() < L)

#Setting up the output
output = '('
for i in range(0, n-1) :
    output += hex(v[i]) + ', '
output += hex(v[n-1]) + ')'

print(output)