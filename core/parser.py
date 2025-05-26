def parse_funcion_objetivo(obj):
    """
    Convierte una función objetivo como "6x1+12x2+8x3" en [6, 12, 8]
    """
    obj = obj.replace('-', '+-')
    coef = []
    for term in obj.split('+'):
        term = term.strip()
        if 'x' in term:
            val = term.split('x')[0]
            val = val if val not in ['', '+', '-'] else val + '1'
            coef.append(float(val))
    return coef

def parse_restricciones(texto):
    """
    Convierte texto como:
    2x1+3x2<=60
    4x1+2x2<=80
    En listas: A (coeficientes), b (lado derecho), signos (tipo de restricción)
    """
    A, b, signos = [], [], []
    for line in texto.strip().splitlines():
        line = line.strip()
        if '<=' in line:
            lhs, rhs = line.split('<=')
            signo = '<='
        elif '>=' in line:
            lhs, rhs = line.split('>=')
            signo = '>='
        elif '=' in line:
            lhs, rhs = line.split('=')
            signo = '='
        else:
            continue

        lhs = lhs.replace('-', '+-')
        coefs = []
        for term in lhs.split('+'):
            term = term.strip()
            if 'x' in term:
                val = term.split('x')[0]
                val = val if val not in ['', '+', '-'] else val + '1'
                coefs.append(float(val))
        A.append(coefs)
        b.append(float(rhs.strip()))
        signos.append(signo)

    return A, b, signos
