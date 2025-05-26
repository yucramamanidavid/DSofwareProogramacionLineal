def formatear_funcion_objetivo(c: list[float]) -> str:
    """
    Convierte una lista de coeficientes [4, 6] a una cadena como "4x₁ + 6x₂".
    """
    partes = []
    for i, coef in enumerate(c):
        if coef == 0:
            continue
        signo = "+" if coef > 0 and i > 0 else ""
        termino = f"{signo}{coef}x{i+1}"
        partes.append(termino)
    return " ".join(partes)

def formatear_restriccion(a: list[float], signo: str, rhs: float) -> str:
    """
    Convierte una restricción [2,3], "<=", 6 a "2x₁ + 3x₂ ≤ 6"
    """
    partes = []
    for i, coef in enumerate(a):
        if coef == 0:
            continue
        signo_coef = "+" if coef > 0 and i > 0 else ""
        partes.append(f"{signo_coef}{coef}x{i+1}")
    lhs = " ".join(partes)
    simbolo = "≤" if signo == "<=" else "≥" if signo == ">=" else "="
    return f"{lhs} {simbolo} {rhs}"

def redondear_lista(numeros, decimales=2):
    """
    Redondea todos los números de una lista o matriz a N decimales.
    """
    if isinstance(numeros[0], list):  # matriz
        return [[round(num, decimales) for num in fila] for fila in numeros]
    else:
        return [round(num, decimales) for num in numeros]
