import random
from datetime import datetime
from sympy import legendre_symbol

random.seed(datetime.now().timestamp())

# p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
# g = 2
# q = p-1
# x = random.randint(1, q)
# h = pow(g, x, p)    #Joueur PKEY

# h_bot = int(input("PKEY BOT = "), 16)   # On récupère la PKEY du bot
# print()

# # Définition de la liste des coups
# moves = { 
#             "P": (int.from_bytes("PIERRE".encode(), "big") % p), 
#             "F": (int.from_bytes("FEUILLE".encode(), "big") % p),
#             "C": (int.from_bytes("CISEAUX".encode(), "big") % p)
#         }

# # PROLOGUE
# print("PKEY", hex(h)[2:], "\n")  #Message d'envoi de la PKEY

# i = 0
# while(True) :
#     # Si c'est le tour du joueur
#     if (i % 2) == 0 :
#         m = input("PIERRE = P | FEUILLE = F | CISEAUX = C | STOP = S\t")
        
#         if(m == "S") :
#             break
        
#         # On choisit un aléa
#         k = random.randint(1, q)
        
#         # On chiffre avec ElGamal
#         r = pow(g, k, p)
#         c = (moves[m] * pow(h, k, p)) % p
        
#         # Messages à envoyer
#         print("COMMIT", hex(r)[2:], hex(c)[2:], "\n")
#         if m == "P" :
#             print("MOVE PIERRE\n")
#         else :
#             if m == "F" :
#                 print("MOVE FEUILLE\n")
#             else :
#                 print("MOVE CISEAUX\n")
           
#         print("OPEN", hex(k)[2:])
        
#     # Sinon c'est le tour du bot
#     else :
#         r_bot = int(input("r du bot ?\t"), 16)
#         c_bot = int(input("c du bot ?\t"), 16)
#         m_bot = input("Move du bot ? p | f | c \t")
#         k_bot = int(input("k du bot ?\t"), 16)
        
#         print()
        
#         # Vérification du COMMIT du bot
#         if (r_bot != pow(g, k_bot, p)) or () :
#             print("REFEREE")
#         else :
#             if c_bot != ((moves[m_bot] * pow(h_bot, k_bot, p)) % p) :
#                 print("REFEREE")
#             else :
#                 print("OK")
                
            
#     i += 1
    
"""
p et q doivent etre grand et q doit etre different de p-1, si q = p-1, en calculant le symbole de Legendre du commit
on peut distinguer si c pierre feuille ou ciseau
-> changer de groupe, generer un nombre aleatoire q de valeur 256 max
-> creer un nombre p multiple de q+1
-> verifier que le symbole de legendre de chacun soit identique
-> symbole de legendre pareil?"""

q2 = 251
p2 = 2*q2 + 1
i = 2
while(True) :
    res = 0
    try :
        res = legendre_symbol(q2, p2)
        if res == -1 :
            break
        print("############ ", i)
    except :
        print(i)
    i+=1
    p2 = i * q2 + 1
    
    
    
print("This is the better q :", hex(q2)[2:])
print("This is the better p :", hex(p2)[2:])


'''
    ON NE PEUT PAS CHANGER DE GROUPE
    
    EN APPLIQUANT LE SYMBOLE DE LEGENDRE SUR DIFFIE HELLMAN DECISIONNEL
    
    (a) Si g^x mod p est un carré <=> x est pair
    (b) legendre(x, p) == 1 <=> x est pair
    
    DANS NOTRE CAS 
    legendre(r, p) = legendre(g^(xy)) donne la parité de k
    legendre(h, p) = legendre(g^(xy)) donne la parité de x
    
    s = m*h^k mod p*
    c = m g^(xk) mod p
    
    comme g est générateur on sait qu'il existe l appartenant à [0, q] tq c = g^l
    donc legendre(c,p) donne la parité de l
    
    c = g^l = m*g^(xk) <=> m = g^(l-xk)
    
    si (l-xk) est pair alors legendre(m, p) = 1
    
    POUR TRICHER :
    je connais h, g, p, q
    je sais que m = g^(l-xk)= g^L
    je sais que legendre(r, p) donne la parité de k
    je sais que legendre(h, p) donne la parité de x
    je sais que legendre(c, p) donne la parité de l
    Donc j'ai la parité de l - xk
    Je connais les 3 m possibles
    Je sais que (l - xk) paire => legendre(m, p) = 1
    
    Donc pour chaque msg possible, je calcule legendre(m, p)
    
'''