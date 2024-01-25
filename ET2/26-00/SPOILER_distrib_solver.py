from hashlib import sha256

# Evie
# Générer des bits aléatoires après Evie

# Trouver 2 chaines qui commence par le même nom
# Hash des 2 chaines, les 56 premiers bits sont égaux
# Donc il y a plusieurs clé possible

# Les 2 chaines = 2 clés

# Faut juste trouver le même Hash pour les 2 chaines


# f = la fonction qu'on doit écrire qui fait le hash et qui renvoie les 56 premiers bits
# x0 = le point de départ : un mot aléatoire

def floyd(f, x0) -> (int, int):
    """Floyd's cycle detection algorithm."""
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    # The hare moves twice as quickly as the tortoise and
    # the distance between them increases by 1 at each step.
    # Eventually they will both be inside the cycle and then,
    # at some point, the distance between them will be
    # divisible by the period λ.
    tortoise = f(x0)  # f(x0) is the element/node next to x0.
    hare = f(f(x0))
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))

    # At this point the tortoise position, ν, which is also equal
    # to the distance between hare and tortoise, is divisible by
    # the period λ. So hare moving in cycle one step at a time,
    # and tortoise (reset to x0) moving towards the cycle, will
    # intersect at the beginning of the cycle. Because the
    # distance between them is constant at 2ν, a multiple of λ,
    # they will agree as soon as the tortoise reaches index μ.

    # Find the position μ of first repetition.

    tortoise = x0
    while tortoise != hare:
        m1 = tortoise  # l'étape juste avant car c'est la clé, et l'étape d'après ça hash et ça détecte la colision
        tortoise = f(tortoise)
        hare = f(hare)   # Hare and tortoise move at same speed

    # Find the length of the shortest cycle starting from x_μ
    # The hare moves one step at a time while tortoise is still.
    # lam is incremented until λ is found.

    hare = f(tortoise)
    while tortoise != hare:
        m2 = hare
        hare = f(hare)

    prefix = "Evie"
    m1 = prefix + m1
    m2 = prefix + m2
    print(m1.encode().hex(), m2.encode().hex())


def f(x):
    Pref = "Evie"
    x = Pref + x
    # Calculer le hash de x
    # retourne les 56 premiers bits
    return sha256(x.encode()).hexdigest()[:14]  # 56 bits = 14 hexa = 14*4 = 56 bits


floyd(f, "LIP6")

