import os
import openai
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

openai.api_key = "" #Clave de OpenAi

# Descripción de la vivienda 🏠
def generar_descripcion(habitaciones, banos, estilo, presupuesto):
    """Genera una descripción de la vivienda usando GPT-4 (modelo de chat)."""
    prompt = f"Genera una descripción precisa de una vivienda ideal con {habitaciones} habitaciones, {banos} baños, estilo {estilo}, y un presupuesto de ${presupuesto}."
    try:
        response = openai.ChatCompletion.create(  # Usar el modelo de chat adecuado
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en diseño arquitectónico."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()  # Acceso correcto a la respuesta de chat
    except Exception as e:
        return f"Error al generar la descripción: {e}"

# Generación del plano arquitectónico 🏗️
def generar_plano_imagen(habitaciones, banos, estilo):
    """Genera un plano arquitectónico usando DALL·E."""
    prompt = f"Plano arquitectónico de una vivienda con {habitaciones} habitaciones, {banos} baños, en estilo {estilo}."
    try:
        response = openai.Image.create(  # Utilizar Image.create para generar imágenes
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response["data"][0]["url"]
        img_response = requests.get(image_url)
        return Image.open(BytesIO(img_response.content))
    except Exception as e:
        st.error(f"Error al generar el plano: {e}")
        return None

# Generación de modelo 3D 🕋
def generar_modelo_3d(habitaciones, banos, estilo):
    """Genera una vista 3D de la vivienda en base al plano generado previamente usando DALL·E."""
    prompt = f"Render 3D fotorrealista de una vivienda con {habitaciones} habitaciones, {banos} baños y estilo {estilo} basado en el plano generado previamente."
    try:
        response = openai.Image.create(  # Utilizar Image.create para generar imágenes
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response["data"][0]["url"]
        img_response = requests.get(image_url)
        return Image.open(BytesIO(img_response.content))
    except Exception as e:
        st.error(f"Error al generar el modelo 3D: {e}")
        return None

# Interfaz con Streamlit
# Estilos CSS personalizados
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech&display=swap');
        body { background-color: #ffffff; color: #1f1f1f; font-family: 'Share Tech', sans-serif; margin: 0; padding: 0; }
        .header { background-color: #1f1f1f; color: #fff; padding: 25px; text-align: center; font-size: 36px; font-weight: bold; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); margin-bottom: 30px; font-family: 'Share Tech', sans-serif; }
        .footer { background-color: #222; color: white; text-align: center; padding: 20px; font-size: 16px; position: relative; margin-top: 40px; box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.1); font-family: 'Share Tech', sans-serif; }
        .stButton>button { background-color: #1f1f1f; color: white; padding: 12px 24px; font-size: 18px; border: 1px solid black; cursor: pointer; transition: background-color 0.3s ease, transform 0.2s ease; font-family: 'Share Tech', sans-serif; }
        .stButton>button:hover { background-color: #ffffff; color: #1f1f1f; border: 1px solid black; }
        .expanderHeader { font-size: 22px; font-weight: bold; font-family: 'Share Tech', sans-serif; color: #1f1f1f; }
        .expanderContent { padding: 20px; font-family: 'Share Tech', sans-serif; background-color: #1f1f1f; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }
        .stImage img { box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1); }
        .stMarkdown { font-size: 16px; line-height: 1.6; color: #1f1f1f; font-family: 'Share Tech', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">🏠 Steel Block Generator</div>', unsafe_allow_html=True)
st.subheader("Genera planos y modelos 3D de viviendas según tus especificaciones.")

# Información para el usuario
with st.expander("ℹ️ Cómo funciona esta app"):
    st.markdown("""
    ### 🚀 **Cómo funciona Steel Block Generator**

    Steel Block Generator es una herramienta basada en IA que te ayuda a diseñar viviendas con solo unos clics.
    Simplemente ingresa tus preferencias y la aplicación generará:

    - ✅ **Descripción detallada** de la vivienda según los parámetros ingresados.
    - ✅ **Plano arquitectónico** generado con inteligencia artificial.
    - ✅ **Modelo 3D** para visualizar mejor el diseño.

    ### 🛠 **Pasos para generar tu diseño**
    1️⃣ Selecciona el **número de habitaciones**, **baños**, **estilo arquitectónico** y **presupuesto**.
    2️⃣ Haz clic en **"Generar diseño"**.
    3️⃣ Explora la **descripción generada**, el **plano arquitectónico** y la **vista 3D**.

    💡 *Ideal para arquitectos, diseñadores y cualquier persona en busca de inspiración para su próxima vivienda.*
    """, unsafe_allow_html=True)

habitaciones = st.number_input("Número de habitaciones", min_value=1, max_value=10, value=3)
banos = st.number_input("Número de baños", min_value=1, max_value=5, value=2)
estilo = st.selectbox("Estilo arquitectónico", ["Moderno", "Minimalista", "Rústico", "Industrial"])
presupuesto = st.number_input("Presupuesto (en USD)", min_value=10000, max_value=100000, value=50000)

if st.button("Generar diseño"):
    st.subheader("Descripción de la vivienda")
    descripcion = generar_descripcion(habitaciones, banos, estilo, presupuesto)
    st.write(descripcion)
    st.subheader("Plano arquitectónico")
    imagen_plano = generar_plano_imagen(habitaciones, banos, estilo)
    if imagen_plano:
        st.image(imagen_plano, caption="Plano arquitectónico", use_container_width=True)
    st.subheader("Modelo 3D")
    imagen_3d = generar_modelo_3d(habitaciones, banos, estilo)
    if imagen_3d:
        st.image(imagen_3d, caption="Modelo 3D", use_container_width=True)

# Footer
st.markdown('<div class="footer">© 2025 Steel Block Generator | Todos los derechos reservados</div>', unsafe_allow_html=True)