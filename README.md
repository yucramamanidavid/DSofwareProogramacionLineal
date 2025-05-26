# Optimizador Lineal Web

![Banner](https://example.com/banner.jpg) <!-- Reemplazar con imagen real si existe -->

Sistema web académico para resolver problemas de Programación Lineal desarrollado por David Robert Yucra Mamani para la Universidad Peruana Unión - Filial Juliaca.

## 📌 Descripción

Herramienta educativa interactiva que resuelve problemas de optimización lineal mediante tres métodos:

1. **Método Gráfico** (para 2 variables)
2. **Método Simplex Directo** (para múltiples variables)
3. **Método Simplex con Tabla** (paso a paso)

## 🎯 Objetivos

- Implementar una herramienta web práctica y visual
- Facilitar el aprendizaje desde el enfoque gráfico hasta el método Simplex
- Proporcionar retroalimentación clara y detallada

## 🛠️ Tecnologías utilizadas

- **Backend**: Python + Flask
- **Matemáticas**: NumPy + SciPy
- **Visualización**: Plotly
- **Frontend**: HTML5, CSS3, Bootstrap

## 📦 Estructura del proyecto
DSofwareProogramacionLineal/
├── app.py # Aplicación principal Flask
├── grafico.py # Lógica método gráfico
├── simplex.py # Implementación simplex directo
├── simplex_tabla.py # Simplex paso a paso
├── templates/ # Vistas HTML
│ ├── index.html # Página principal
│ ├── grafico.html # Vista método gráfico
│ ├── simplex.html # Vista simplex directo
│ └── simplex_tabla.html# Vista simplex tabla
├── static/ # Archivos estáticos
└── requirements.txt # Dependencias


## ⚙️ Requisitos e instalación

### Pre-requisitos
- Python 3.9+
- pip (gestor de paquetes)

### Instalación paso a paso

1. Clonar repositorio:
```bash
git clone https://github.com/yucramamanidavid/DSofwareProogramacionLineal.git
cd DSofwareProogramacionLineal
Instalar dependencias:

bash
pip install -r requirements.txt
Ejecutar aplicación:

bash
python app.py
Abrir en navegador:

http://127.0.0.1:5000
🖥️ Uso del sistema
Seleccionar método de solución

Ingresar función objetivo (ej: 3x1 + 4x2)

Especificar si es Maximización o Minimización

Agregar restricciones mediante formularios dinámicos

Hacer clic en "Resolver"

Visualizar resultados:

Gráfico interactivo (método gráfico)

Solución directa (simplex)

Tablas iterativas (simplex tabla)

📚 Métodos implementados
1. Método Gráfico (grafico.py)
Entrada: Función objetivo + hasta 5 restricciones en x₁ y x₂

Salida:

Gráfico interactivo con Plotly

Rectas de restricciones

Región factible sombreada

Vértices evaluados

Punto óptimo marcado

2. Método Simplex Directo (simplex.py)
Tecnología: scipy.optimize.linprog

Ventajas:

Soporta múltiples variables

Resultados rápidos

Identifica casos no factibles/no acotados

3. Método Simplex con Tabla (simplex_tabla.py)
Características:

Implementación manual del algoritmo

Muestra cada iteración con:

Tablas completas

Variables básicas/no básicas

Cálculo de Cj - Zj

Ratios y pivotes

Explicación textual de cada paso

🚨 Solución de problemas
Si python no funciona, probar con python3

Para errores de instalación:

bash
python -m pip install --upgrade pip
Crear entorno virtual (recomendado):

bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
📝 Observaciones
Código modularizado y documentado

Interfaz responsiva

Validación de entradas

Mensajes de error descriptivos

📜 Licencia
Proyecto académico desarrollado para el curso de Análisis Multivariado - Universidad Peruana Unión © 2025

✉️ Contacto
Autor: David Robert Yucra Mamani
Asesor: Ing. Milton Edward Humpiri Flores
Institución: Facultad de Ingeniería y Arquitectura - Escuela Profesional de Ingeniería de Sistemas
Ubicación: Juliaca, Perú - Mayo 2025
