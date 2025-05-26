import numpy as np
from scipy.optimize import linprog
from .parser import parse_funcion_objetivo, parse_restricciones

def resolver_simplex(objetivo, restricciones_texto, tipo='max'):
    c = parse_funcion_objetivo(objetivo)
    A, b, signos = parse_restricciones(restricciones_texto)

    # Validación rápida
    if not all(len(row) == len(c) for row in A):
        return "<p>Error: número de variables en restricciones no coincide con función objetivo.</p>"

    # Separar restricciones según tipo
    A_ub, b_ub = [], []
    A_eq, b_eq = [], []

    for i, signo in enumerate(signos):
        if signo == "<=":
            A_ub.append(A[i])
            b_ub.append(b[i])
        elif signo == ">=":
            A_ub.append([-a for a in A[i]])  # Convertir a <=
            b_ub.append(-b[i])
        elif signo == "=":
            A_eq.append(A[i])
            b_eq.append(b[i])

    # Convertir a arrays si no están vacíos
    A_ub = np.array(A_ub) if A_ub else None
    b_ub = np.array(b_ub) if b_ub else None
    A_eq = np.array(A_eq) if A_eq else None
    b_eq = np.array(b_eq) if b_eq else None

    c_np = np.array(c)
    if tipo == 'max':
        c_np = -c_np  # linprog minimiza por defecto

    bounds = [(0, None)] * len(c_np)

    res = linprog(
        c=c_np,
        A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq,
        bounds=bounds,
        method='highs'
    )

    if res.success:
        resultado = "<h4>✅ Solución óptima encontrada:</h4><ul>"
        for i, val in enumerate(res.x):
            estado = " (básica)" if val > 1e-6 else " (no básica)"
            resultado += f"<li>x{i+1} = {val:.2f}{estado}</li>"

        z = -res.fun if tipo == 'max' else res.fun
        resultado += f"<li><strong>Valor óptimo Z = {z:.2f}</strong></li>"
        resultado += f"<li>Iteraciones realizadas: {res.nit}</li>"

        # Estado del solver en lenguaje claro
        mensaje = res.message.lower()
        if "optimal" in mensaje:
            resultado += f"<li>Estado: solución óptima encontrada exitosamente.</li>"
        elif "infeasible" in mensaje:
            resultado += f"<li style='color:red;'>Estado: el problema no tiene solución factible.</li>"
        elif "unbounded" in mensaje:
            resultado += f"<li style='color:red;'>Estado: el problema no está acotado (solución infinita).</li>"
        else:
            resultado += f"<li><em>Estado técnico del solver:</em> {res.message}</li>"

        if np.all(res.x < 1e-6):
            resultado += "<li><em>Advertencia: todas las variables quedaron en cero. Puede ser una solución degenerada.</em></li>"

        resultado += "</ul>"
    else:
        resultado = "<p style='color:red;'><strong>❌ No se encontró una solución factible.</strong></p>"
        resultado += f"<p><strong>Estado del solver:</strong> {res.message}</p>"

    return resultado
