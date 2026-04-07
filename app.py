import streamlit as st
from groq import Groq

SYSTEM_PROMPT = """
Eres un analista experto en corporate venture building con experiencia en identificar 
oportunidades de negocio para grandes corporaciones. Tu metodología combina análisis 
de tendencias macro, detección de pain points reales de usuarios y diseño de conceptos 
de venture viables.

Cuando el usuario te dé un SECTOR y opcionalmente un CLIENTE CORPORATIVO, debes 
generar un brief de oportunidad estructurado exactamente así:

---
## 🔍 BRIEF DE OPORTUNIDAD

**Sector:** [sector introducido]  
**Cliente:** [cliente o "genérico" si no se especifica]

---

### 📈 3 Tendencias clave
1. [Tendencia con dato o señal concreta]
2. [Tendencia con dato o señal concreta]
3. [Tendencia con dato o señal concreta]

---

### 😤 2 Pain points no resueltos
1. **[Nombre del problema]:** [descripción en 2 líneas desde el punto de vista del usuario]
2. **[Nombre del problema]:** [descripción en 2 líneas desde el punto de vista del usuario]

---

### 💡 3 Conceptos de venture

**Venture 1 — [Nombre sugerido]**
- Qué es: [una frase]
- Para quién: [segmento concreto]
- Por qué ahora: [razón de timing]
- Modelo de negocio: [cómo gana dinero]

**Venture 2 — [Nombre sugerido]**
- Qué es: [una frase]
- Para quién: [segmento concreto]
- Por qué ahora: [razón de timing]
- Modelo de negocio: [cómo gana dinero]

**Venture 3 — [Nombre sugerido]**
- Qué es: [una frase]
- Para quién: [segmento concreto]
- Por qué ahora: [razón de timing]
- Modelo de negocio: [cómo gana dinero]

---

### ⚡ Oportunidad destacada
[En 3-4 líneas, cuál de los tres conceptos tiene más potencial y por qué, 
siendo directo y argumentado]

---
Sé siempre concreto, evita generalidades. Usa ejemplos reales del sector cuando puedas.
"""

st.set_page_config(page_title="Venture Opportunity Scanner", page_icon="🔍", layout="wide")

if "historial" not in st.session_state:
    st.session_state.historial = []

# Layout: columna principal + sidebar con historial
col_main, col_hist = st.columns([2, 1])

with col_main:
    st.title("🔍 Venture Opportunity Scanner")
    st.caption("Genera briefs de oportunidad de negocio en segundos")

    sector = st.text_input("Sector", placeholder="ej. alimentación y restauración")
    cliente = st.text_input("Cliente corporativo (opcional)", placeholder="ej. Heineken")

    if st.button("Generar brief", type="primary"):
        if not sector:
            st.warning("Introduce el sector.")
        else:
            with st.spinner("Analizando oportunidades..."):
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    user_input = f"Sector: {sector}."
                    if cliente:
                        user_input += f" Cliente: {cliente}."

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    resultado = response.choices[0].message.content

                    # Guardar en historial
                    etiqueta = f"{sector}" + (f" · {cliente}" if cliente else "")
                    st.session_state.historial.insert(0, {
                        "etiqueta": etiqueta,
                        "sector": sector,
                        "cliente": cliente,
                        "resultado": resultado
                    })

                    st.markdown(resultado)

                except Exception as e:
                    st.error(f"Error: {e}")

with col_hist:
    st.subheader("📋 Historial")

    if not st.session_state.historial:
        st.caption("Aún no hay briefs generados.")
    else:
        if st.button("🗑️ Limpiar historial"):
            st.session_state.historial = []
            st.rerun()

        for i, item in enumerate(st.session_state.historial):
            with st.expander(f"{'🟢' if i == 0 else '⚪'} {item['etiqueta']}"):
                st.markdown(item["resultado"])
