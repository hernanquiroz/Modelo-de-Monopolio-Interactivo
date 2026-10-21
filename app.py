import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ───────────────────────────────────────────────────────────────
# Configuración de la página
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Monopolio Interactivo",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────
# Título y descripción
# ──────────────────────────────────────────────────────────────
st.title("🏭 Monopolio (Interactivo)")
st.markdown("""
Analiza el comportamiento de un **monopolista** y sus decisiones de precio y cantidad.
- 🔵 **Demanda (D)**: Curva de demanda del mercado
- 🔵 **Ingreso Marginal (IMg)**: Ingreso adicional por vender una unidad más
- 🔴 **Costo Marginal (CMg)**: Costo adicional de producir una unidad más
- ⚫ **Equilibrio**: Donde IMg = CMg (cantidad óptima), precio leído de la demanda
""")

# ─────────────────────────────────────────────────────────────
# Parámetros base del modelo
# ──────────────────────────────────────────────────────────────
st.sidebar.header("️ Parámetros Base")

# Demanda: P = a - b*Q
a_base = st.sidebar.number_input("Intercepto Demanda (a)", value=10.0, step=0.5)
b = st.sidebar.number_input("Pendiente Demanda (b)", value=1.0, step=0.1)

# Costo Marginal: CMg = c + d*Q
c_base = st.sidebar.number_input("Intercepto CMg (c)", value=2.0, step=0.5)
d = st.sidebar.number_input("Pendiente CMg (d)", value=0.5, step=0.1)

st.sidebar.markdown("---")

# ───────────────────────────────────────────────────────────────
# Desplazamientos de curvas
# ──────────────────────────────────────────────────────────────
st.sidebar.header(" Desplazamientos de Curvas")

delta_D = st.sidebar.slider(
    "Desplazamiento Demanda (Δa)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

delta_CMg = st.sidebar.slider(
    "Desplazamiento CMg (Δc)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Leyenda:**")
st.sidebar.markdown("🔵 Sólida = Demanda (D)")
st.sidebar.markdown("🔵 Punteada = Ingreso Marginal (IMg)")
st.sidebar.markdown("🔴 Sólida = Costo Marginal (CMg)")
st.sidebar.markdown("⚫ Punto = Equilibrio del monopolista")

# ───────────────────────────────────────────────────────────────
# Calcular curvas con desplazamientos
# ──────────────────────────────────────────────────────────────
Q = np.linspace(0, 10, 200)

# Parámetros actuales
a_actual = a_base + delta_D
c_actual = c_base + delta_CMg

# Demanda: P = a - b*Q
P_D = a_actual - b * Q

# Ingreso Marginal: IMg = a - 2b*Q (misma intersección, doble pendiente)
P_IMg = a_actual - 2 * b * Q

# Costo Marginal: CMg = c + d*Q
P_CMg = c_actual + d * Q

# ───────────────────────────────────────────────────────────────
# Calcular equilibrio del monopolista
# ──────────────────────────────────────────────────────────────
# Condición: IMg = CMg
# a - 2b*Q = c + d*Q
# Q* = (a - c) / (2b + d)

Q_monop = (a_actual - c_actual) / (2 * b + d)
P_monop = a_actual - b * Q_monop  # Precio de la demanda
CMg_monop = c_actual + d * Q_monop  # Debe ser igual a IMg
IMg_monop = a_actual - 2 * b * Q_monop

# Equilibrio de competencia perfecta (para comparación)
# D = CMg → a - b*Q = c + d*Q → Q* = (a-c)/(b+d)
Q_comp = (a_actual - c_actual) / (b + d)
P_comp = a_actual - b * Q_comp

# Equilibrio original (sin desplazamientos)
Q_orig = (a_base - c_base) / (2 * b + d)
P_orig = a_base - b * Q_orig

# ──────────────────────────────────────────────────────────────
# Mostrar métricas
# ──────────────────────────────────────────────────────────────
st.markdown("###  Equilibrio del Monopolista")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Cantidad Óptima (Q*)",
        value=f"{Q_monop:.2f}",
        delta=f"{Q_monop - Q_orig:+.2f} vs original"
    )

with col2:
    st.metric(
        label="Precio de Monopolio (P*)",
        value=f"{P_monop:.2f}",
        delta=f"{P_monop - P_orig:+.2f} vs original"
    )

with col3:
    markup = P_monop - CMg_monop
    st.metric(
        label="Markup (P - CMg)",
        value=f"{markup:.2f}",
        help="Diferencia entre precio y costo marginal"
    )

st.markdown("---")

# ───────────────────────────────────────────────────────────────
# Crear la gráfica
# ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))

# Grid
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_axisbelow(True)

# Curva de Demanda (azul sólida)
ax.plot(Q, P_D, 'b-', linewidth=2.5, 
        label=f'Demanda (D) [Δ={delta_D:+.1f}]')

# Ingreso Marginal (azul punteada)
ax.plot(Q, P_IMg, 'b--', linewidth=2.5, 
        label=f'Ingreso Marginal (IMg)')

# Costo Marginal (rojo sólido)
ax.plot(Q, P_CMg, 'r-', linewidth=2.5, 
        label=f'Costo Marginal (CMg) [Δ={delta_CMg:+.1f}]')

# Punto de equilibrio del monopolista (donde IMg = CMg)
ax.plot(Q_monop, P_monop, 'ko', markersize=12, 
        markeredgecolor='black', markerfacecolor='black', 
        markeredgewidth=2, zorder=10)

# Líneas punteadas desde el equilibrio
ax.axhline(y=P_monop, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax.axvline(x=Q_monop, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# Punto de competencia perfecta (para comparación)
ax.plot(Q_comp, P_comp, 'gs', markersize=10, 
        markeredgecolor='darkgreen', markerfacecolor='lightgreen', 
        markeredgewidth=2, zorder=9, label='Competencia Perfecta')

# Etiqueta del punto de equilibrio
ax.annotate(f'Eq. Monopolio\n(Q={Q_monop:.1f}, P={P_monop:.1f})', 
            xy=(Q_monop, P_monop), 
            xytext=(Q_monop + 0.8, P_monop + 0.8),
            fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Configuración de ejes
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('Cantidad (Q)', fontsize=13, fontweight='bold')
ax.set_ylabel('Precio / Costo (P, C)', fontsize=13, fontweight='bold')
ax.set_title('Monopolio (Interactivo)', 
             fontsize=15, fontweight='bold', pad=20)

# Leyenda
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

# Marcas en los ejes
ax.set_xticks(np.arange(0, 11, 2))
ax.set_yticks(np.arange(0, 11, 2))

plt.tight_layout()

# ───────────────────────────────────────────────────────────────
# Mostrar gráfica en Streamlit
# ──────────────────────────────────────────────────────────────
st.pyplot(fig)

# ───────────────────────────────────────────────────────────────
# Análisis comparativo
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### ⚖️ Monopolio vs Competencia Perfecta")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🏭 Monopolio**")
    st.markdown(f"""
    - **Cantidad:** Q* = {Q_monop:.2f}
    - **Precio:** P* = {P_monop:.2f}
    - **Condición:** IMg = CMg
    - **Características:**
      - Menor cantidad producida
      - Mayor precio cobrado
      - Poder de mercado
      - Genera pérdida de peso muerto
    """)

with col2:
    st.markdown("**🏪 Competencia Perfecta**")
    st.markdown(f"""
    - **Cantidad:** Q* = {Q_comp:.2f}
    - **Precio:** P* = {P_comp:.2f}
    - **Condición:** P = CMg
    - **Características:**
      - Mayor cantidad producida
      - Menor precio cobrado
      - Sin poder de mercado
      - Eficiencia asignativa
    """)

# Diferencia
diff_Q = Q_comp - Q_monop
diff_P = P_monop - P_comp

st.info(f"""
**📊 Diferencia:**
- El monopolista produce **{diff_Q:.2f} unidades menos** que en competencia perfecta
- El monopolista cobra **{diff_P:.2f} más** que en competencia perfecta
""")

# ──────────────────────────────────────────────────────────────
# Interpretación económica
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📚 Interpretación Económica")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🔵 Curva de Demanda (D)**")
    if delta_D > 0:
        st.success(f"""
        **✅ Aumento de demanda** (Δ = {delta_D:+.1f})
        
        **Causas:**
        - ↑ Preferencias de consumidores
        - ↑ Ingreso de consumidores
        - ↑ Población
        - Campañas publicitarias exitosas
        
        **Efectos:**
        - ↑ Cantidad producida
        - ↑ Precio cobrado
        - ↑ Beneficios del monopolista
        """)
    elif delta_D < 0:
        st.error(f"""
        **️ Disminución de demanda** (Δ = {delta_D:+.1f})
        
        **Causas:**
        - ↓ Preferencias
        - ↓ Ingreso
        - Productos sustitutos más baratos
        
        **Efectos:**
        - ↓ Cantidad producida
        - ↓ Precio cobrado
        - ↓ Beneficios
        """)
    else:
        st.info("➡️ Demanda en posición original")

with col2:
    st.markdown("**🔴 Costo Marginal (CMg)**")
    if delta_CMg > 0:
        st.error(f"""
        **️ Aumento de costos** (Δ = {delta_CMg:+.1f})
        
        **Causas:**
        - ↑ Precios de insumos
        - ↑ Salarios
        - ↑ Impuestos
        - Regulaciones más estrictas
        
        **Efectos:**
        - ↓ Cantidad producida
        - ↑ Precio cobrado
        - ↓ Beneficios (posible)
        """)
    elif delta_CMg < 0:
        st.success(f"""
        **✅ Disminución de costos** (Δ = {delta_CMg:+.1f})
        
        **Causas:**
        - Avance tecnológico
        - ↓ Precios de insumos
        - Economías de escala
        - Mejora en productividad
        
        **Efectos:**
        - ↑ Cantidad producida
        - ↓ Precio cobrado
        - ↑ Beneficios
        """)
    else:
        st.info("➡️ CMg en posición original")

# ───────────────────────────────────────────────────────────────
# Poder de mercado
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("###  Poder de Mercado (Índice de Lerner)")

# Índice de Lerner: L = (P - CMg) / P
if P_monop > 0:
    Lerner = (P_monop - CMg_monop) / P_monop
else:
    Lerner = 0

st.markdown(f"""
El **Índice de Lerner** mide el poder de mercado del monopolista:

**L = (P - CMg) / P = ({P_monop:.2f} - {CMg_monop:.2f}) / {P_monop:.2f} = {Lerner:.3f}**
""")

if Lerner > 0.5:
    st.warning(f"""
    **⚠️ Alto poder de mercado** (L = {Lerner:.3f})
    
    El monopolista tiene gran capacidad para fijar precios por encima del costo marginal.
    """)
elif Lerner > 0.2:
    st.info(f"""
    **📊 Poder de mercado moderado** (L = {Lerner:.3f})
    
    El monopolista tiene capacidad significativa para fijar precios.
    """)
else:
    st.success(f"""
    **✅ Bajo poder de mercado** (L = {Lerner:.3f})
    
    El monopolista tiene limitada capacidad para fijar precios (mercado casi competitivo).
    """)

st.markdown("""
**Interpretación:**
- L = 0: Competencia perfecta (P = CMg)
- L = 1: Monopolio puro con poder absoluto
- 0 < L < 1: Poder de mercado intermedio
""")

# ──────────────────────────────────────────────────────────────
# Escenarios predefinidos
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎯 Escenarios de Política y Mercado")

scenario = st.selectbox(
    "Selecciona un escenario:",
    ["Selecciona...",
     "1. Aumento de Demanda (Publicidad)",
     "2. Recesión (Caída de Demanda)",
     "3. Aumento de Costos (Impuestos)",
     "4. Avance Tecnológico (↓ Costos)",
     "5. Regulación de Precios (P = CMg)",
     "6. Monopolio Natural"]
)

if scenario == "1. Aumento de Demanda (Publicidad)":
    st.success(" **Campaña publicitaria exitosa**")
    st.markdown("- La demanda se desplaza hacia la **derecha** (Δ = +2.0)")
    st.markdown("- El IMg también se desplaza")
    st.markdown("- **Resultado:** ↑Q, ↑P, ↑Beneficios")
    st.markdown(f"- **Sugerencia:** Δa = +2.0")

elif scenario == "2. Recesión (Caída de Demanda)":
    st.error("📉 **Recesión económica**")
    st.markdown("- La demanda se desplaza hacia la **izquierda** (Δ = -2.0)")
    st.markdown("- Menor disposición a pagar")
    st.markdown("- **Resultado:** ↓Q, ↓P, ↓Beneficios")
    st.markdown(f"- **Sugerencia:** Δa = -2.0")

elif scenario == "3. Aumento de Costos (Impuestos)":
    st.error("️ **Impuesto al monopolista**")
    st.markdown("- El CMg se desplaza hacia **arriba** (Δ = +1.5)")
    st.markdown("- Mayor costo de producción")
    st.markdown("- **Resultado:** ↓Q, ↑P, ↓Beneficios")
    st.markdown(f"- **Sugerencia:** Δc = +1.5")

elif scenario == "4. Avance Tecnológico (↓ Costos)":
    st.success("🔧 **Innovación tecnológica**")
    st.markdown("- El CMg se desplaza hacia **abajo** (Δ = -1.5)")
    st.markdown("- Menor costo de producción")
    st.markdown("- **Resultado:** ↑Q, ↓P, ↑Beneficios")
    st.markdown(f"- **Sugerencia:** Δc = -1.5")

elif scenario == "5. Regulación de Precios (P = CMg)":
    st.info("️ **Regulación gubernamental**")
    st.markdown("- El gobierno obliga a fijar P = CMg")
    st.markdown("- El monopolista produce como en competencia perfecta")
    st.markdown("- **Resultado:** Q = Q_comp, P = P_comp")
    st.markdown("- Elimina la pérdida de peso muerto")
    st.markdown(f"- **Cantidad regulada:** {Q_comp:.2f}")
    st.markdown(f"- **Precio regulado:** {P_comp:.2f}")

elif scenario == "6. Monopolio Natural":
    st.warning("🏭 **Monopolio natural**")
    st.markdown("- Costos fijos muy altos, costos marginales bajos")
    st.markdown("- Un solo productor es más eficiente")
    st.markdown("- **Ejemplos:** Servicios públicos (agua, electricidad)")
    st.markdown("- Requiere regulación para proteger consumidores")

# ───────────────────────────────────────────────────────────────
# Ecuaciones
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📐 Ecuaciones del Modelo")

col1, col2, col3 = st.columns(3)

with col1:
    st.latex(rf"\text{{Demanda: }} P = {a_actual:.1f} - {b}Q")

with col2:
    st.latex(rf"\text{{IMg: }} P = {a_actual:.1f} - {2*b}Q")

with col3:
    st.latex(rf"\text{{CMg: }} P = {c_actual:.1f} + {d}Q")

st.markdown(f"""
**Equilibrio del Monopolista (IMg = CMg):**
- Q* = {Q_monop:.2f}
- P* = {P_monop:.2f}
- CMg = {CMg_monop:.2f}

**Competencia Perfecta (P = CMg):**
- Q* = {Q_comp:.2f}
- P* = {P_comp:.2f}
""")

# ───────────────────────────────────────────────────────────────
# Conceptos clave
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📖 Conceptos Clave")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🏭 Monopolio**")
    st.markdown("Un solo vendedor")
    st.markdown("Barrera de entrada")
    st.markdown("Fijador de precios")
    st.markdown("IMg < P")

with col2:
    st.markdown("**⚖️ Condición de Equilibrio**")
    st.markdown("IMg = CMg")
    st.markdown("Maximiza beneficios")
    st.markdown("No produce donde P = CMg")
    st.markdown("Genera pérdida de peso muerto")

with col3:
    st.markdown("**🏪 Competencia Perfecta**")
    st.markdown("Muchos vendedores")
    st.markdown("Sin barreras")
    st.markdown("Tomador de precios")
    st.markdown("P = CMg")
