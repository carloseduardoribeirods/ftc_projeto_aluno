# ================================================
# Imports
# ================================================

import pandas as pd
import plotly.express as px
import inflection
import streamlit as st
from PIL import Image

# =================================================
# Page config
# =================================================

st.set_page_config(page_title='Visão Cuisines',
                   page_icon='🍝',
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

# ==============================
# Code functions
# ==============================

# Função para selecionar as avaliações dos melhores restaurantes

def cuisines_metric(cuisines_name, df1):
    rows = df1['cuisines'] == cuisines_name
    cols = ['restaurant_id', 'aggregate_rating', 'restaurant_name']
    df_aux = (df1.loc[rows, cols].groupby('restaurant_id')
                                 .max()
                                 .reset_index()
                                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True]))
    first_row = df_aux.iloc[0]
    aggregate_rating = first_row['aggregate_rating']
    info_str = f" {aggregate_rating}/5.0"
    
    return df_aux, info_str
# Função para gerar gráfico de barras

def generate_bar_chart(df1, ascending):
    
    title = 'melhores' if not ascending else 'piores'
      
    df_aux = (df1[['cuisines', 'aggregate_rating']].groupby('cuisines')
                                                   .max()
                                                   .reset_index()
                                                   .sort_values('aggregate_rating', ascending = ascending))

    df_limitado = df_aux.head(10)

                   # Plotando o gráfico de barras
    fig = px.bar(df_limitado, x='cuisines', y='aggregate_rating', text='aggregate_rating', title=f'Top 10 {title} tipos de culinárias')

        # Atualizando o título dos eixos, remoção de linhas de grade e ajuste do tamanho da fonte dos eixos X e Y
    fig.update_xaxes(title_text='Culinárias', tickfont=dict(size=18), showgrid = False)
    fig.update_yaxes(title_text='Avaliação média', tickfont=dict(size=18), showgrid = False)

        # Adicionando rótulos de dados e ajuste no tamanho da fonte
    fig.update_traces(texttemplate='%{text}', textfont=dict(size=20))

        # Centralizando o título, definição de tamanho do gráfico, tamanho da fonte do título e legendas do eixo X e Y
    fig.update_layout(title_x=0.5,
                      height=600,
                      title_font=dict(size=24),
                      xaxis_title_font=dict(size=16),
                      yaxis_title_font=dict(size=16))

    st.plotly_chart(fig, use_container_width = True)

# =================================================
# Layout
# =================================================
st.header('🍝 Marketplace - Visão Cozinhas')

image_path = 'logo.jpg'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=240)
                
st.sidebar.markdown('# iRango Food Company')
st.sidebar.markdown('## O melhor lugar para encontrar aquele prato de chef!')
st.sidebar.markdown("""---""")
st.sidebar.markdown('# Filtro de paises')


# Criando o filtro de países
countries = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']

countries_default = ['England', 'Brazil', 'South Africa', 'Qatar', 'Canada', 'Australia']

country_options = st.sidebar.multiselect('Selecione os paises desejados', options = countries , default = countries)

# Criando o limitador do filtro de países

countries_selected = []
countries_selected = df1['country_code'].isin(country_options)
df1 = df1.loc[countries_selected, :]

st.sidebar.markdown("""---""")

# Criando o filtro de número de restaurantes

num_items = st.sidebar.slider('Selecione o número de restaurantes que deseja visualiar', value=10, min_value=1, max_value=20)

filtered_df = df1.head(num_items)

st.sidebar.markdown("""---""")

# Criando o filtro de cidades

cuisines = ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian', 'Author',
       'Gourmet Fast Food', 'Lebanese', 'Modern Australian', 'African',
       'Coffee and Tea', 'Australian', 'Middle Eastern', 'Malaysian',
       'Tapas', 'New American', 'Pub Food', 'Southern', 'Diner', 'Donuts',
       'Southwestern', 'Sandwich', 'Irish', 'Mediterranean', 'Cafe Food',
       'Korean BBQ', 'Fusion', 'Canadian', 'Breakfast', 'Cajun',
       'New Mexican', 'Belgian', 'Cuban', 'Taco', 'Caribbean', 'Polish',
       'Deli', 'British', 'California', 'Others', 'Eastern European',
       'Creole', 'Ramen', 'Ukrainian', 'Hawaiian', 'Patisserie',
       'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan', 'Burmese',
       'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian', 'Continental',
       'South Indian', 'North Indian', 'Salad', 'Finger Food', 'Mandi',
       'Turkish', 'Kerala', 'Pakistani', 'Biryani', 'Street Food',
       'Nepalese', 'Goan', 'Iranian', 'Mughlai', 'Rajasthani', 'Mithai',
       'Maharashtrian', 'Gujarati', 'Rolls', 'Momos', 'Parsi',
       'Modern Indian', 'Andhra', 'Tibetan', 'Kebab', 'Chettinad',
       'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi', 'Afghan',
       'Lucknowi', 'Charcoal Chicken', 'Mangalorean', 'Egyptian',
       'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian', 'Western',
       'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian', 'Balti',
       'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji', 'South African',
       'Durban', 'World Cuisine', 'Izgara', 'Home-made', 'Giblets',
       'Fresh Fish', 'Restaurant Cafe', 'Kumpir', 'Döner',
       'Turkish Pizza', 'Ottoman', 'Old Turkish Bars', 'Kokoreç']

cuisines_default = ['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian']


cuisines_options = st.sidebar.multiselect('Selecione o tipo de gastronomia', options = cuisines, default = cuisines_default)
                                       
cuisines_selected = []
cuisines_selected = df1['cuisines'].isin(cuisines_options)
df1 = df1.loc[cuisines_selected, :]
                                       
st.sidebar.markdown("""---""")

tab1, tab2, tab3 = st.tabs(['Visão Cuisines', '_', '_'])
with tab1:
    
        col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        
        for col, cuisine in zip([col1, col2, col3, col4, col5], ['Italian', 'American', 'Arabian', 'Japanese', 'Brazilian']):
            with col:
                                
                df_aux, info_str = cuisines_metric(cuisine, df1)  # Chama a função para obter df_aux e info_str
                
                st.metric(f'{cuisine.capitalize()}: {df_aux.iloc[0]["restaurant_name"]}', info_str)

    
        cols = ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating']
        df_aux = df1[cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True])
        ranking = df_aux.head(num_items)
        st.header("Top 10 Restaurantes")
        st.write(ranking)       
    
        col1, col2 = st.columns(2, gap='small')  
        with col1:
            generate_bar_chart(df1, ascending=False)
        with col2:
            generate_bar_chart(df1, ascending=True)
        

        