# DEFECTO 5 - Estilo: nombres no descriptivos, magic numbers, logica duplicada

def p(l):
    r = []
    for i in l:
        if i > 0:
            r.append(i * 1.16)
    return r

def calc(l):
    r = []
    for i in l:
        if i > 0:
            r.append(i * 1.16)
    return r

def descuento(precio, d):
    return precio - (precio * d / 100)