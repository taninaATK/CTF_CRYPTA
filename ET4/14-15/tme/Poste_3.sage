from sage.rings.finite_rings.integer_mod import square_root_mod_prime_power
from sage.modules.free_module_integer import IntegerLattice

#Problem info
p = 0xf121527bb3d5ae8e84b9507bc066bd9bf054804c963986729f8a6e14c7cb1de7a3a3caafc4fd9c17d6a3319e0a4f4de59abe06c86b17e6cf30ff5f6a6796de725f700e40d520a8c1ac93944ad38bb305e0686ee90eb46f87bd8e6603695be1e99e408e725459d9c9a2f79d8c85f0f75584929cbb9c2241eba5d494e3c6f5df5d

#Finding beta s.t (a ** 2) == (beta ** 2) mod p
ok = False
test = Mod(-1, p)
beta = square_root_mod_prime_power(test, p, 1)
beta = int(beta)
print((p - 1) == pow(beta, 2, p))


#Creating the matrix associated to this problem
m = Matrix([[p, 0],[beta, 1]])

# LLL reducing because it's funlll & coolll & chilll
mlll = IntegerLattice(m);
#print(mlll)
v = mlll.shortest_vector(algorithm="fplll")

#Print the output
print(v)