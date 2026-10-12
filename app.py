import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import json, re, time

# --- CONFIG ---
st.set_page_config(page_title="ChipiIA Nube", layout="centered")
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "PEGA_AQUI_TU_KEY_DE_GEMINI_TEMPORAL")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

MAPEO = {
    "normal": "Chipi_Base - 😊 Normal",
    "hablando": "Chipi_1 - 🗣️ Hablando",
    "feliz": "Chipi_1 - 😄 Feliz",
    "enojado": "Chipi_2 - 😠 Enojado",
    "sorprendido": "Chipi_3 - 😲 Sorprendido",
    "triste": "Chipi_4 - 😢 Triste",
    "pensando": "Chipi_5 - 🤔 Pensando"
}

st.title("ChipiIA - Cerebro en la Nube")
st.caption("Sin tarjeta, con tus 6 expresiones")

if "historial" not in st.session_state:
    st.session_state.historial = []

pregunta = st.text_input("Dile algo a Chipi:", placeholder="Chipi busca un perro triste")

if st.button("Hablar") and pregunta:
    with st.spinner("Chipi_5 - Pensando..."):
        prompt = f"""Eres Chipi. Responde en español muy corto (max 15 palabras).
        Devuelve SOLO JSON: {{"texto":"respuesta","emocion":"normal|hablando|enojado|sorprendido|triste|pensando","busca_imagen":"si|no","query":"que buscar"}}
        Pregunta: {pregunta}"""
        try:
            resp = model.generate_content(prompt).text
            data = json.loads(re.search(r'\{.*\}', resp, re.DOTALL).group())

            st.success(f"**{MAPEO.get(data['emocion'], 'Chipi_Base')}**")
            st.write(f"### {data['texto']}")

            if data['busca_imagen'] == 'si':
                st.write(f"Buscando: {data['query']}")
                with DDGS() as ddgs:
                    results = list(ddgs.images(data['query'], max_results=1))
                    if results:
                        st.image(results[0]['image'], caption=data['query'], use_column_width=True)

            st.session_state.historial.append((pregunta, data))
        except Exception as e:
            st.error(f"Error: {e} - ¿Pusiste tu GEMINI_KEY en Secrets?")

st.divider()
st.write("Historial de expresiones:")
for q, d in reversed(st.session_state.historial[-5:]):
    st.write(f"- Tú: {q} -> Chipi: {d['texto']} [{d['emocion']}]")