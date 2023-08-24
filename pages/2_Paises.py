# ================================================
# Imports
# ================================================

import pandas as pd
import plotly.express as px
import inflection
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

# =================================================
# Page config
# =================================================

st.set_page_config(page_title='Visão Paises',
                   page_icon='🌎',
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

# Atualização do layout dos gráficos

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
st.header('🌎 Marketplace - Visão Países')

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

tab1, tab2, tab3 = st.tabs(['Visão Países', '_', '_'])

with tab1:
    with st.container():
                    
            # Selecionando os dados
            df_aux = (df1[['restaurant_id', 'country_code']].groupby('country_code')
                                                            .count()
                                                            .reset_index()
                                                            .sort_values('restaurant_id', ascending = False))

            # Plotando o gráfico de barras
            fig = px.bar(df_aux, x='country_code', y='restaurant_id', text='restaurant_id', title='Quantidade de restaurantes registrados por país')

            # Atualizando o título dos eixos, remoção de linhas de grade e ajuste do tamanho da fonte dos eixos X e Y
            fig.update_xaxes(title_text='Países', showgrid=False, tickfont=dict(size=18))
            fig.update_yaxes(title_text='Quantidade de Restaurantes', showgrid=False, tickfont=dict(size=18))
            
            # Executa a função que atualiza o layout do gráfico
            fig_update(df1, fig)
            
            st.plotly_chart(fig, use_container_width = True)
            
            # Selecionando os dados
            df_aux = (df1[['city', 'country_code']].groupby('country_code')
                                                   .nunique()
                                                   .reset_index()
                                                   .sort_values('city', ascending = False))
 
            # Plotando o gráfico de barras
            fig = px.bar(df_aux, x='country_code', y='city', text='city', title='Quantidade de cidades registradas por país')

            # Atualiando o títulos dos eixos
            fig.update_xaxes(title_text='Países', tickfont=dict(size=18), showgrid=False)
            fig.update_yaxes(title_text='Cidades', tickfont=dict(size=18), showgrid=False)

            # Executa a função que atualiza o layout do gráfico
            fig_update(df1, fig)
            
            st.plotly_chart(fig, use_container_width = True)
        
    with st.container():
        col1, col2 = st.columns(2, gap='small')
        
        with col1:
            # Selecionando os dados
            df_aux = (round(df1[['votes', 'country_code']].groupby('country_code')
                                                          .mean(), 2)
                                                          .reset_index()
                                                          .sort_values('votes', ascending = False))
            # Plotando o gráfico de barras
            fig = px.bar(df_aux, x='country_code', y='votes', text='votes', title='Média de avaliações feitas por país')

            # Atualizando o títulos dos eixos
            fig.update_xaxes(title_text='Países', tickfont=dict(size=18), showgrid=False)
            fig.update_yaxes(title_text='Avaliações', tickfont=dict(size=18), showgrid=False)

            # Executa a função que atualiza o layout do gráfico
            fig_update(df1, fig)
            
            st.plotly_chart(fig, use_container_width = True)
            
        with col2:
            # Selecionando os dados
            df_aux = (round(df1[['average_cost_for_two', 'country_code']].groupby('country_code')
                                                                         .mean(), 2)
                                                                         .reset_index()
                                                                         .sort_values('average_cost_for_two', ascending = False))

            # Plotando o gráfico de barras
            fig = px.bar(df_aux, x='country_code', y='average_cost_for_two', text='average_cost_for_two', title='Preço médio de um prato para duas pessoas por país')

            # Atualizando os títulos dos eixos
            fig.update_xaxes(title_text='Países', tickfont=dict(size=18), showgrid=False)
            fig.update_yaxes(title_text='Custo médio do prato para 2 pessoas', tickfont=dict(size=18), showgrid=False)
            
            # Executa a função que atualiza o layout do gráfico
            fig_update(df1, fig)
            
            st.plotly_chart(fig, use_container_width = True)