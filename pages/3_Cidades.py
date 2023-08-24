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

st.set_page_config(page_title='Visão Cidades',
                   page_icon='🏙️',
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

# Criação das cores por país para utilização em gráficos

cor_por_pais = {
        "India": 'red',
        "Australia": 'blue',
        "Brazil": 'green',
        "Canada": 'purple',
        "Indonesia": 'orange',
        "New Zeland": 'cyan',
        "Philippines": 'pink',
        "Qatar": 'brown',
        "Singapure": 'magenta',
        "South Africa": 'gray',
        "Sri Lanka": 'lime',
        "Turkey": 'yellow',
        "United Arab Emirates": 'teal',
        "England": 'indigo',
        "United States of America": 'black'
    }
cor_por_pais_invertido = {
    'red': 'India',
    'blue': 'Australia',
    'green': 'Brazil',
    'purple': 'Canada',
    'orange': 'Indonesia',
    'cyan': 'New Zeland',
    'pink': 'Philippines',
    'brown': 'Qatar',
    'magenta': 'Singapure',
    'gray': 'South Africa',
    'lime': 'Sri Lanka',
    'yellow': 'Turkey',
    'teal': 'United Arab Emirates',
    'indigo': 'England',
    'black': 'United States of America'
}

# Gerando gráficos de barras

def generate_bar_chart(df1, rows_condition, title_suffix, color_column=None):
        # Selecionando os dados
    
    cols = ['restaurant_id', 'city', 'aggregate_rating', 'country_code']

    df_aux = (df1.loc[rows_condition, cols].groupby(['country_code','city'])
                                           .count()
                                           .reset_index()
                                           .sort_values(['restaurant_id', 'city'], ascending = [False, True]))
    if color_column:
        df_aux['color'] = df_aux[color_column].map(cor_por_pais)
    df_limitado = df_aux.head(7)
    
    title = f'Top 7 Cidades com mais restaurantes {title_suffix}'
    # Plotando o gráfico de barras

    fig = px.bar(df_limitado, x='city', y='restaurant_id', text='aggregate_rating', title=title, color='country_code' if color_column else None)

    # Atualizando o título dos eixos, remoção de linhas de grade e ajuste do tamanho da fonte dos eixos X e Y
    fig.update_xaxes(title_text='Cidades', tickfont=dict(size=18), showgrid = False)
    fig.update_yaxes(title_text='Restaurantes', tickfont=dict(size=18), showgrid = False)

        # Adicionando rótulos de dados e ajuste no tamanho da fonte
    fig.update_traces(texttemplate='%{text}', textfont=dict(size=20))

        # Centralizando o título, definição de tamanho do gráfico, tamanho da fonte do título e legendas do eixo X e Y
    fig.update_layout(title_x=0.5,
                      height=600,
                      title_font=dict(size=24),
                      xaxis_title_font=dict(size=16),
                      yaxis_title_font=dict(size=16))
        
        

    st.plotly_chart(fig, use_container_width = True)

# Atualização de layout dos gráficos

def fig_update(df1 ,fig):
            # Adicionando rótulos de dados e ajuste no tamanho da fonte
    fig.update_traces(texttemplate='%{text}', textfont=dict(size=20))

        # Centralizando o título, definição de tamanho do gráfico, tamanho da fonte do título e legendas do eixo X e Y
    fig.update_layout(title_x=0.5,
                      height=600,
                      title_font=dict(size=24),
                      xaxis_title_font=dict(size=16),
                      yaxis_title_font=dict(size=16))
    
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
st.header('🏙️ Marketplace - Visão Cidades')

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

countries_default = ['Qatar', 'England', 'South Africa', 'Canada', 'Australia', 'Brazil']

country_options = st.sidebar.multiselect('Selecione os paises desejados', options = countries , default = countries_default)

# Criando o limitador do filtro de países

countries_selected = []
countries_selected = df1['country_code'].isin(country_options)
df1 = df1.loc[countries_selected, :]

tab1, tab2, tab3 = st.tabs(['Visão Cidades', '_', '_'])


with tab1:
    with st.container():
        
        # Selecionando os dados
         
        df_aux = (df1[['city', 'restaurant_id', 'country_code']].groupby(['country_code','city'])
                                                                .count()
                                                                .reset_index()
                                                                .sort_values(by=['restaurant_id', 'city'], ascending = [False, True]))
        df_aux['color'] = df_aux['country_code'].map(cor_por_pais)
        df_limitado = df_aux.head(10)
            

        # Plotando o gráfico de barras
        fig = px.bar(df_limitado, x='city', y='restaurant_id', text='restaurant_id', title='Top 10 Cidades com mais restaurantes registrados por país', color='country_code')

        # Atualizando o título dos eixos, remoção de linhas de grade e ajuste do tamanho da fonte dos eixos X e Y
        fig.update_xaxes(title_text='Cidades', tickfont=dict(size=18), showgrid = False)
        fig.update_yaxes(title_text='Quantidade de Restaurantes', tickfont=dict(size=18), showgrid = False)

        fig_update(df1, fig)

        st.plotly_chart(fig, use_container_width = True)

    
    with st.container():
        

    
        col1, col2 = st.columns(2, gap='small')
        with col1:
            generate_bar_chart(df1, df1['aggregate_rating'] >= 4, 'com média acima de 4', 'country_code')         
                
        with col2:
            generate_bar_chart(df1, df1['aggregate_rating'] <= 2.5, 'com média abaixo de 2.5', 'country_code')
           
            
    with st.container():

        # Top 10 Cidades que possui a maior quantidade de tipos de culinária distintas
        df_aux = (df1[['city', 'cuisines', 'country_code']].groupby(['country_code', 'city'])
                                                           .nunique()
                                                           .reset_index()
                                                           .sort_values(['cuisines', 'country_code'], ascending = [False, True]))
        df_aux['color'] = df_aux['country_code'].map(cor_por_pais)
        df_limitado = df_aux.head(10)            

        fig = px.bar(df_limitado, x='city', y='cuisines', text='cuisines', title='Top 10 Cidades com mais quantidade de tipos de culinárias distintas', color='country_code')

        # Atualizando o título dos eixos, remoção de linhas de grade e ajuste do tamanho da fonte dos eixos X e Y
        fig.update_xaxes(title_text='Cidades', tickfont=dict(size=18), showgrid = False)
        fig.update_yaxes(title_text='Culinárias distintas', tickfont=dict(size=18), showgrid = False)

        fig_update(df1, fig)
        
        st.plotly_chart(fig, use_container_width = True)
