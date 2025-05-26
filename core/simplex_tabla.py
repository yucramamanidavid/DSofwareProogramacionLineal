import numpy as np
import pandas as pd
from .parser import parse_funcion_objetivo, parse_restricciones

MAX_ITERACIONES = 20  # Seguridad contra ciclos infinitos

def construir_tabla(A, b, c):
    m, n = A.shape
    tabla = np.hstack([A, np.identity(m), b.reshape(-1, 1)])
    cj = np.concatenate([c, np.zeros(m + 1)])  # c + slack + RHS
    base_idx = list(range(n, n + m))  # Índices de holguras en base inicial
    return tabla, cj, base_idx

def calcular_z(tabla, cj, base_idx):
    filas_base = [np.where(tabla[:, i] == 1)[0][0] for i in base_idx]
    z = np.sum(tabla[filas_base, :-1] * cj[base_idx][:, None], axis=0)
    zcj = cj[:-1] - z
    return np.append(zcj, 0)

def iteracion_simplex(tabla, cj, base_idx):
    zcj = calcular_z(tabla, cj, base_idx)
    explicacion = ""

    if np.all(zcj[:-1] <= 1e-8):
        explicacion = "✅ Todos los valores de Cj - Zj son ≤ 0. Se alcanzó la solución óptima.\n"
        return tabla, base_idx, zcj, True, None, None, explicacion

    col_piv = np.argmax(zcj[:-1])
    cjzj_val = zcj[col_piv]
    explicacion += f"📌 Columna pivote seleccionada: x{col_piv + 1} (Cj - Zj = {cjzj_val:.2f})\n"

    ratios = []
    for i in range(len(tabla)):
        if tabla[i, col_piv] > 0:
            ratio = tabla[i, -1] / tabla[i, col_piv]
            ratios.append(ratio)
        else:
            ratios.append(np.inf)

    if all(r == np.inf for r in ratios):
        explicacion += "\n⚠ No hay fila válida para pivote. El problema es no acotado."
        return tabla, base_idx, zcj, True, None, None, explicacion

    fila_piv = np.argmin(ratios)
    explicacion += "\n📊 Cálculo de ratios (RHS / columna pivote):\n"
    for i, ratio in enumerate(ratios):
        val = f"{ratio:.2f}" if ratio != np.inf else "∞"
        explicacion += f"  - Fila {i+1}: {tabla[i, -1]:.2f} / {tabla[i, col_piv]:.2f} = {val}\n"

    var_entrante = f"x{col_piv + 1}"
    var_saliente = f"x{base_idx[fila_piv]+1}" if base_idx[fila_piv] < len(cj) - 1 else f"S{base_idx[fila_piv] + 1 - len(cj)}"
    explicacion += f"\n🔄 Entra a la base: {var_entrante}, sale: {var_saliente}\n"
    explicacion += f"➡️ Fila pivote seleccionada: {fila_piv + 1}\n"

    # Actualización de tabla
    pivote = tabla[fila_piv, col_piv]
    tabla[fila_piv, :] /= pivote
    for i in range(len(tabla)):
        if i != fila_piv:
            tabla[i, :] -= tabla[i, col_piv] * tabla[fila_piv, :]

    base_idx[fila_piv] = col_piv
    zcj = calcular_z(tabla, cj, base_idx)
    terminado = np.all(zcj[:-1] <= 1e-8)

    return tabla, base_idx, zcj, terminado, col_piv, fila_piv, explicacion

def resaltar_pivote(df, fila_piv, col_piv):
    """Devuelve tabla HTML con celda pivote resaltada por posición."""
    def estilo_html(val, i, j):
        if i == fila_piv and j == col_piv:
            return f'<td style="background-color: #fff3cd; font-weight: bold; border:1px solid #dee2e6;">{val:.2f}</td>'
        return f'<td style="border:1px solid #dee2e6;">{val:.2f}</td>'

    headers = ''.join(f'<th style="background:#e9ecef; border:1px solid #dee2e6;">{col}</th>' for col in df.columns)
    index_labels = df.index.tolist()

    rows_html = ""
    for i, idx in enumerate(index_labels):
        fila = df.iloc[i]
        row_cells = ''.join(estilo_html(fila[j], i, j) for j in range(len(fila)))
        rows_html += f'<tr><th style="background:#f8f9fa; border:1px solid #dee2e6;">{idx}</th>{row_cells}</tr>\n'

    tabla_html = f"""
    <div style="overflow-x:auto;">
    <table class="table table-sm table-hover" style="border-collapse: collapse; margin-top: 10px;">
      <thead><tr><th></th>{headers}</tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    </div>
    """
    return tabla_html


def resolver_simplex_tabla(objetivo, restricciones_texto, tipo="max"):
    c = parse_funcion_objetivo(objetivo)
    A, b, signos = parse_restricciones(restricciones_texto)

    if tipo == 'min':
        c = [-ci for ci in c]

    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    tabla, cj, base_idx = construir_tabla(A, b, c)
    pasos = []
    terminado = False
    iteracion = 0

    while not terminado and iteracion < MAX_ITERACIONES:
        iteracion += 1
        tabla, base_idx, zcj, terminado, col_piv, fila_piv, explicacion = iteracion_simplex(tabla, cj, base_idx)

        columnas = [f"x{i+1}" for i in range(A.shape[1])] + [f"S{i+1}" for i in range(A.shape[0])] + ["RHS"]
        base_vars = [f"x{i+1}" if i < len(c) else f"S{i+1-len(c)}" for i in base_idx]
        df = pd.DataFrame(tabla, columns=columnas, index=base_vars)
        df.loc['Cj-Zj'] = zcj

        # Convertir tabla a HTML con celda pivote resaltada
        tabla_html = resaltar_pivote(df, fila_piv, col_piv) if fila_piv is not None else df.to_html(classes="table table-bordered", border=1)

        pasos.append((iteracion, tabla_html, col_piv, fila_piv, explicacion))

    if iteracion >= MAX_ITERACIONES:
        pasos.append((iteracion, df.to_html(classes="table table-bordered", border=1), None, None, "⚠ Se alcanzó el máximo de iteraciones. Posible ciclado o degeneración."))
        valor_optimo = None
    else:
        valor_optimo = tabla[:, -1].dot(cj[base_idx])
        if tipo == 'min':
            valor_optimo = -valor_optimo

    return pasos, valor_optimo
