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

st.set_page_config(page_title="Venture Opportunity Scanner", page_icon="🔍")
st.title("🔍 Venture Opportunity Scanner")
st.caption("Genera briefs de oportunidad de negocio en segundos")

api_key = st.text_input("API Key de Groq", type="password")
sector = st.text_input("Sector", placeholder="ej. alimentación y restauración")
cliente = st.text_input("Cliente corporativo (opcional)", placeholder="ej. Heineken")

if st.button("Generar brief", type="primary"):
    if not api_key or not sector:
        st.warning("Introduce la API key y el sector.")
    else:
        with st.spinner("Analizando oportunidades..."):
            try:
                client = Groq(api_key=api_key)
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
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
