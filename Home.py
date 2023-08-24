import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
    
)

image_path = 'logo.jpg'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=240)

st.sidebar.markdown('# iRango Food Company')
st.sidebar.markdown('## O melhor lugar para encontrar aquele prato de chef!')
st.sidebar.markdown("""---""")

st.write( "# Fome Zero Dashboard" )

st.markdown(
    """
    Fome Zero Dashboard foi construído para acompanhar as métricas de crescimento dos restaurantes.
    ### Como utilizar esse Dashboard?
    - Visão Geral:
        - Métricas gerais do negócio.
        - Mapa com a localização central dos restaurantes, clusterizados por região e categorizados por avaliação (cor).
    - Visão Paises:
        - Volume de restaurantes por país.
        - Avaliação média por país.
        - Custo médio do prato para 2 pessoas por país.
    - Visão Cidades:
        - Volume de restaurantes por cidade.
        - Ranking de melhores e piores restaurantes por cidades e avaliação média.
        - Volume de culinárias distintas por cidade.
    - Visão Cozinhas:
        - Restaurantes com melhor avaliação por melhor tipo de culinária.
        - Os 10 restaurantes mais bem avaliados.
        - Os melhores e piores tipos de culinárias.
    ### Ask for Help
    - Time de Data Science no Discord
        - @Cadu
""" )
