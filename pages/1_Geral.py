# ================================================
# Imports
# ================================================

import pandas as pd
import plotly.express as px
import inflection
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# =================================================
# Page config
# =================================================

st.set_page_config(page_title='Visão Geral',
                   page_icon='📈',
                   layout='wide',
                   initial_sidebar_state='auto')

# =================================================
# File upload
# =================================================

# Executando a leitura dos dados
df = pd.read_csv('datasets/zomato.csv')

# Salvando uma cópia dos dados originais
df1 = df.copy()

# =================================================
# Functions
# =================================================

# Preenchimento do nome dos países
COUNTRIES = {
  1: "India",
  14: "Australia",
  30: "Brazil",
  37: "Canada",
  94: "Indonesia",
  148: "New Zeland",
  162: "Philippines",
  166: "Qatar",
  184: "Singapure",
  189: "South Africa",
  191: "Sri Lanka",
  208: "Turkey",
  214: "United Arab Emirates",
  215: "England",
  216: "United States of America",
}

def country_name(country_id):
  return COUNTRIES[country_id]

# Criação do tipo de categoria de comida
def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
   return "normal"
  elif price_range == 3:
    return "expensive"
  else:
   return "gourmet"


# Criação do nome das cores

COLORS = {
  "3F7E00": "darkgreen",
  "5BA829": "green",
  "9ACD32": "lightgreen",
  "CDD614": "orange",
  "FFBA00": "red",
  "CBCBC8": "darkred",
  "FF7800": "darkred",
}
def color_name(color_code):
  return COLORS[color_code]
# Formatando as colunas

def rename_columns(df):

  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df1.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df1.columns = cols_new

  return df1

# Renomeando as colunas
df1 = rename_columns(df)

# =================================================
# Applying functions
# =================================================

# Substitui os códigos de países pelos nomes respectivos
df1['country_code'] = df1['country_code'].apply(country_name)

# Define categorias de preço de acordo com o range
df1['price_range'] = df1['price_range'].apply(create_price_tye)

# Define o padrão de cores das avaliações
df1['rating_color'] = df1['rating_color'].apply(color_name)
    
# =================================================
# Dataframe cleaning
# =================================================

# Removendo linhas vazias
df1 = df1.dropna(subset=['cuisines'])

# Definindo os restaurantes por apenas um tipo de culinária
df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])

# Removendo a coluna 'Switch to order menu', pois todos os valores eram iguais.
df1 = df1.drop(columns = ['switch_to_order_menu'], axis = 1)

# Removendo linhas duplicadas
df1 = df1.drop_duplicates().reset_index()

# Removendo Cuisines do tipo Mineira e Drinks Only
df1 = df1.loc[(df1['cuisines'] != 'Drinks Only') & (df1['cuisines'] != 'Mineira'), :]
    
# =================================================
# Layout
# =================================================
st.header('📈 Marketplace - Visão Geral')

image_path = 'logo.jpg'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=240)
                
st.sidebar.markdown('# iRango Food Company')
st.sidebar.markdown('## O melhor lugar para encontrar aquele prato de chef!')
st.sidebar.markdown("""---""")

st.sidebar.markdown('# Filtro de paises)')

countries = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']

country_options = st.sidebar.multiselect('Selecione os paises desejados', options = countries , default = countries)

tab1, tab2, tab3 = st.tabs(['Visão Geral', '_', '_'])

with tab1:
    with st.container():
        st.title('Métricas gerais')
        col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        
        with col1:            
            # Restaurantes únicos resgitrados

            restaurantes = df1['restaurant_id'].nunique()
            col1.metric('Restaurantes registrados', restaurantes)
        
        with col2:
            # Países únicos registrados
            
            paises = df1['country_code'].nunique()
            col2.metric('Países registrados', paises)
            
        with col3:
            # Cidades únicas registradas
            cidades = df1['city'].nunique()
            col3.metric('Cidades registradas', cidades)
            
        with col4:
            # Total de avaliações registradas
            avaliacoes = df1['votes'].sum()
            col4.metric('Avaliações registradas', avaliacoes)
            
        with col5:
            # Total de culinárias registradas
            culinarias = df1['cuisines'].nunique()
            col5.metric('Culinárias registradas', culinarias)
        
    with st.container():
        st.header('Localização central de restaurantes clusterizados por região e categorizados (cor) pela avaliação média')
        
        f = folium.Figure(width=1920, height=1080)
        map = folium.Map(zoom_start=11, max_bounds=True).add_to(f)
        marker_cluster = MarkerCluster().add_to(map)

        for index, marker_info in df1.iterrows():
            # Formatando os marcadores com HTML
            popup_content = f'''
            <div style="width: 300px">
                            <b>ID do Restaurante:</b> {marker_info['restaurant_id']}<br>
                            <b>Nome do Restaurante:</b> {marker_info['restaurant_name']}<br>
                            <b>País:</b> {marker_info['country_code']}<br>
                            <b>Cidade:</b> {marker_info['city']}<br>
                            <b>Custo Médio para Dois:</b> {marker_info['average_cost_for_two']} {marker_info['currency']}<br>
                            <b>Faixa de Preço:</b> {marker_info['price_range']}<br>
                            <b>Avaliação Agregada:</b> {marker_info['aggregate_rating']}
            </div>
            '''
            # Plotando o mapa
            folium.Marker([marker_info['latitude'],
                         marker_info['longitude']],
                         popup=folium.Popup(popup_content, max_width=300),
                         icon=folium.Icon(color=marker_info['rating_color'])).add_to(marker_cluster)
                   
        folium_static( map, width = 1024, height = 600 )