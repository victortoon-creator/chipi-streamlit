import streamlit as st, google.generativeai as genai, json, re
from duckduckgo_search import DDGS

st.set_page_config(page_title="ChipiIA", layout="centered")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

VIDEOS = {
  "normal": "Chipi_Base.mp4", "base": "Chipi_Base.mp4",
  "hablando": "Chipi_1.mp4", "feliz": "Chipi_1.mp4",
  "enojado": "Chipi_2.mp4", "sorprendido": "Chipi_3.mp4",
  "triste": "Chipi_4.mp4", "pensando": "Chipi_5.mp4"
}

st.title("ChipiIA - Cerebro en la Nube")
q = st.text_input("Dile algo a Chipi:", "Chipi estoy feliz")

if st.button("Hablar") and q:
    prompt = f'SOLO JSON {{"texto":"respuesta corta","emocion":"normal|hablando|enojado|sorprendido|triste|pensando"}} Pregunta: {q}'
    data = json.loads(re.search(r'\{{.*\}}', model.generate_content(prompt).text, re.DOTALL).group())
    video = VIDEOS.get(data['emocion'], "Chipi_Base.mp4")
    st.video(video, autoplay=True, loop=True, muted=True)
    st.write(f"### {data['texto']} - {data['emocion']}")
