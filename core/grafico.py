import plotly.graph_objs as go
import numpy as np
import itertools

def parse_funcion_objetivo(obj):
    obj = obj.replace('-', '+-')
    coef = [0, 0]
    for term in obj.split('+'):
        term = term.strip()
        if 'x1' in term:
            val = term.replace('x1', '')
            coef[0] = float(val) if val not in ['', '+', '-'] else float(val + '1')
        elif 'x2' in term:
            val = term.replace('x2', '')
            coef[1] = float(val) if val not in ['', '+', '-'] else float(val + '1')
    return coef

def parse_restricciones(lines):
    restricciones = []
    for line in lines.strip().splitlines():
        if "<=" in line:
            lhs, rhs = line.split("<=")
            signo = "<="
        elif ">=" in line:
            lhs, rhs = line.split(">=")
            signo = ">="
        elif "=" in line:
            lhs, rhs = line.split("=")
            signo = "="
        else:
            continue

        lhs = lhs.replace('-', '+-')
        a, b = 0, 0
        for term in lhs.split('+'):
            term = term.strip()
            if 'x1' in term:
                val = term.replace('x1', '')
                a = float(val) if val not in ['', '+', '-'] else float(val + '1')
            elif 'x2' in term:
                val = term.replace('x2', '')
                b = float(val) if val not in ['', '+', '-'] else float(val + '1')
        restricciones.append((a, b, signo, float(rhs)))
    return restricciones

def punto_interseccion(r1, r2):
    a1, b1, _, c1 = r1
    a2, b2, _, c2 = r2
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([c1, c2])
    try:
        x = np.linalg.solve(A, B)
        return x if np.all(x >= 0) else None
    except np.linalg.LinAlgError:
        return None

def cumple_todas(punto, restricciones):
    x, y = punto
    for a, b, signo, c in restricciones:
        val = a*x + b*y
        if signo == "<=" and val > c + 1e-6:
            return False
        if signo == ">=" and val < c - 1e-6:
            return False
        if signo == "=" and abs(val - c) > 1e-6:
            return False
    return True

def ordenar_puntos(puntos):
    puntos = np.array(puntos)
    centro = np.mean(puntos, axis=0)
    return sorted(puntos, key=lambda p: np.arctan2(p[1] - centro[1], p[0] - centro[0]))

def resolver_metodo_grafico(objetivo, restricciones, tipo):
    c = parse_funcion_objetivo(objetivo)
    restr = parse_restricciones(restricciones)

    puntos_factibles = []

    for r1, r2 in itertools.combinations(restr, 2):
        p = punto_interseccion(r1, r2)
        if p is not None and cumple_todas(p, restr):
            puntos_factibles.append(tuple(p))

    # Intersecciones con ejes
    for a, b, signo, rhs in restr:
        if a != 0:
            x0 = rhs / a
            if x0 >= 0 and cumple_todas((x0, 0), restr):
                puntos_factibles.append((x0, 0))
        if b != 0:
            y0 = rhs / b
            if y0 >= 0 and cumple_todas((0, y0), restr):
                puntos_factibles.append((0, y0))

    # Redondear para evitar duplicados flotantes
    puntos_unicos = list({(round(p[0], 6), round(p[1], 6)) for p in puntos_factibles})
    info = "<ul>"
    optimo = None
    valor_optimo = None
    if len(puntos_unicos) >= 1:
        puntos_array = np.array(puntos_unicos)
        z_vals = [c[0]*x + c[1]*y for x, y in puntos_array]
        for i, (xv, yv) in enumerate(puntos_array):
            info += f"<li>Vértice {i+1}: ({xv:.2f}, {yv:.2f}) → Z = {z_vals[i]:.2f}</li>"

        idx = np.argmax(z_vals) if tipo == 'max' else np.argmin(z_vals)
        optimo = puntos_array[idx]
        valor_optimo = z_vals[idx]
        info += "</ul>"

        traces = []

        # Rango dinámico para líneas
        if puntos_unicos:
            xs, ys = zip(*puntos_unicos)
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            margen = 0.2
            x_margin = (x_max - x_min) * margen if x_max != x_min else 1
            y_margin = (y_max - y_min) * margen if y_max != y_min else 1
            x_range = np.linspace(max(0, x_min - x_margin), x_max + x_margin, 500)
        else:
            x_range = np.linspace(0, 10, 500)

        # Líneas de restricciones
        for a, b, signo, rhs in restr:
            if b != 0:
                y_vals = (rhs - a * x_range) / b
                traces.append(go.Scatter(x=x_range, y=y_vals, mode='lines',
                                         name=f"{a}x₁ + {b}x₂ {signo} {rhs}"))
            else:
                x_val = rhs / a
                traces.append(go.Scatter(x=[x_val, x_val], y=[0, max(ys) + y_margin],
                                         mode='lines',
                                         name=f"{a}x₁ + {b}x₂ {signo} {rhs}"))

        # Región factible
        if len(puntos_unicos) >= 3:
            ordenados = np.array(ordenar_puntos(puntos_unicos))
            x_poly = np.append(ordenados[:, 0], ordenados[0, 0])
            y_poly = np.append(ordenados[:, 1], ordenados[0, 1])
            traces.append(go.Scatter(x=x_poly, y=y_poly,
                                     fill='toself',
                                     fillcolor='rgba(200,200,200,0.4)',
                                     line=dict(color='gray'),
                                     name='Región Factible'))

        # Vértices
        traces.append(go.Scatter(x=puntos_array[:, 0],
                                 y=puntos_array[:, 1],
                                 mode='markers+text',
                                 text=[f"Z={z:.2f}" for z in z_vals],
                                 name='Vértices',
                                 marker=dict(size=8)))

        # Punto óptimo
        traces.append(go.Scatter(x=[optimo[0]], y=[optimo[1]],
                                 mode='markers+text',
                                 name='Óptimo',
                                 marker=dict(size=12, color='red'),
                                 text=[f"Óptimo: Z={valor_optimo:.2f}"]))

        layout = go.Layout(title="Método Gráfico",
                           xaxis=dict(title='x₁', autorange=True),
                           yaxis=dict(title='x₂', autorange=True),
                           legend=dict(x=0, y=1),
                           hovermode='closest')

        fig = go.Figure(data=traces, layout=layout)
        graph_html = fig.to_html(full_html=False)

        html_result = f"""
        <div class="alert alert-success" role="alert" style="font-size: 1.1rem;">
            ✅ <strong>Solución óptima encontrada</strong>
        </div>

        <div style="margin-bottom: 1rem;">
            <strong>📍 Óptimo en:</strong> <code>({optimo[0]:.2f}, {optimo[1]:.2f})</code><br>
            <strong>💡 Valor óptimo Z:</strong> <code>{valor_optimo:.2f}</code>
        </div>

        <div>
            <h5>🔹 Evaluación de Vértices</h5>
            <ul style="line-height: 1.8;">
        """

        for i, (xv, yv, z) in enumerate(zip(puntos_array[:, 0], puntos_array[:, 1], z_vals)):
            estrella = "⭐" if (xv, yv) == tuple(optimo) else ""
            html_result += f"<li>Vértice {i+1}: ({xv:.2f}, {yv:.2f}) → Z = {z:.2f} {estrella}</li>"

        html_result += "</ul></div>"
        html_result += f"<div class='mt-4'>{graph_html}</div>"

        return html_result

    else:
        return "<p>No hay solución factible.</p>"
