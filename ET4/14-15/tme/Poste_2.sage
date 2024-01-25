from sage.modules.free_module_integer import IntegerLattice

#Problem info
n = 2
p = 0xd818b95040d468e81692bb9efcfa076233b3badaee000b71d6904de84fe93f2be5e26e1e5fdfdb1e6450b2b9adc07a90079612f865ffd10db8945cddae1404ffad607e97e830b3bcf07f94298789a0da49672e92274a1a3244486000549953c049bebad8ea629c908106772bab4641d2186eec13f7758affe9e4a3c2b4be4809
x = 0x40048f1ca9f16391858505fa9ad2d74aadfd83628336bb5903dd8aea92a4d3e911e923eac8a655d5b7a1f1160b7de2a9c67edf2c7b43c691ce5827c846c2fedf94dc5144cd26bf86c1e8c0a8d678b848d67071164f2b7f5849414564f179836d3b8a59b99773a30f4b83a5de9149db838df3e378f99aed8a4a5e99a9d0c7a9a0

#Creating the matrix associated to this problem
m = Matrix([[p, 0],[x, 1]])

# LLL reducing because it's funlll & coolll & chilll
mlll = IntegerLattice(m);
#print(mlll)
v = mlll.shortest_vector(algorithm="fplll")

#Print the output
print(v)