import pandas as pd
import folium
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão dos Entregadores', layout='wide')

# =========================
# Funções
# =========================

# TRATAMENTO DOS DADOS

def clean_code(df1):
    """ 
    Esta função limpa o dataframe:
    1. Remove espaço no texto
    2. Excluir linhas com 'NaN '
    3. Modifica os tipos de dados
    4. Trata a coluna de tempo (removendo str do int)
    5. Reseta o index
    
    Input: Dataframe
    Output: Dataframe
    """
    #Removendo espaço no texto de todas as colunas com a função strip()
    for column in df1.columns:
      tipo_coluna = df1[column].dtype
      if tipo_coluna == 'object':
        df1.loc[:,column] = df1.loc[:,column].str.strip()

    # Excluir as linhas com 'NaN '
    colunas_selecionadas = ['Time_Orderd', 'Road_traffic_density', 'multiple_deliveries', 'Festival', 'City', 'Delivery_person_Age']
    for colunas in colunas_selecionadas:
      linhas_vazias = df1[f'{colunas}'] != 'NaN'
      df1 = df1.loc[linhas_vazias, :]

    #Modificando tipo dos dados
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%H:%M:%S')
    df1['Time_Order_picked'] = pd.to_datetime(df1['Time_Order_picked'], format='%H:%M:%S')
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # Removendo parte do texto '(min) ' da coluna Time_taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    # Removendo a parte fixa "conditions "
    df1['Weatherconditions'] = df1['Weatherconditions'].str.replace('conditions ', '')
    
    #Resetando index
    df1 = df1.reset_index( drop=True )
    
    return df1

# DESENVOLVIMENTO DOS DADOS PARA GRÁFICOS E TABELAS

def avaliacao_medio_desvio(df1, cols, group):
    df1_avaliacao_medio_desvio = df1.loc[:,cols].groupby(group).agg(['mean', 'std']).round(2)
    df1_avaliacao_medio_desvio.columns = ['Avaliação Média','Desvio Padrão']
    df1_avaliacao_medio_desvio = df1_avaliacao_medio_desvio.reset_index()
    return df1_avaliacao_medio_desvio
            
def top_10_entregadores(df1, top_asc):
    df1_rapidos_cidade = df1.loc[:,['Delivery_person_ID','Time_taken(min)','City']].groupby(['City','Delivery_person_ID']).mean().sort_values(by=['City','Time_taken(min)'], ascending=top_asc).reset_index()
    df1_rapidos_cidade_urban = df1_rapidos_cidade.loc[df1_rapidos_cidade['City']=='Urban',:].head(10)
    df1_rapidos_cidade_metropolitian = df1_rapidos_cidade.loc[df1_rapidos_cidade['City']=='Metropolitian',:].head(10)
    df1_rapidos_cidade_semiurban = df1_rapidos_cidade.loc[df1_rapidos_cidade['City']=='Semi-Urban',:].head(10)
    df_top_10 = pd.concat([df1_rapidos_cidade_urban, df1_rapidos_cidade_metropolitian, df1_rapidos_cidade_semiurban]).reset_index(drop=True)
    df_top_10.rename(columns={'City':'Cidade','Delivery_person_ID':'ID do Entregador','Time_taken(min)':'Tempo Médio (min)'},inplace=True)
    df_top_10.index = range(1, len(df_top_10) + 1)
    return df_top_10.head(10)

# =========================
# Estrutura Lógica do código
# =========================

# Importando o arquivo
df = pd.read_csv('train.csv')

# Limpando os dados
df1 = clean_code(df)


# =========================
# Streamlit - Barra Lateral
# =========================

image = Image.open('logo.png')
st.sidebar.image(image, width=128)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Selecione um periodo')
date_slider = st.sidebar.slider('Qual o periodo?', value=pd.datetime(2022,3,11), min_value=pd.datetime(2022,2,11), max_value=pd.datetime(2022,4,6), format='DD-MM-YYYY')
st.sidebar.markdown("""---""")

st.sidebar.markdown('### Selecione a condição do trânsito')
opcao_transito =st.sidebar.multiselect('Quais as condições do trânsito?',['Low', 'Medium', 'High', 'Jam'], default=['Low', 'Medium', 'High', 'Jam'])

#Aplicando o filtro de periodo ao Data Frame
filtro_periodo = df1['Order_Date'] < date_slider
df1 = df1.loc[filtro_periodo, :]

#Aplicando o filtro de transito ao Data Frame
filtro_transito = df1['Road_traffic_density'].isin(opcao_transito)
df1 = df1.loc[filtro_transito, :]

# =========================
# Streamlit - Layout
# =========================

with st.container():
    st.header('Visão dos Entregadores')
    col1, col2, col3, col4 = st.columns(4, gap = 'large')
    
    with col1:
        maior_idade = df1['Delivery_person_Age'].max()
        col1.metric(' Maior Idade', maior_idade )
    
    with col2:
        menor_idade = df1['Delivery_person_Age'].min()
        col2.metric('Menor Idade', menor_idade)
        
    with col3:
        melhor_condicao = df1['Vehicle_condition'].max()
        col3.metric('Melhor condição veicular', melhor_condicao)

    with col4:
        pior_condicao = df1['Vehicle_condition'].min()
        col4.metric('Pior condição veicular', pior_condicao)
     
       
    
with st.container():
    st.markdown("""---""")
    st.markdown('#### Avaliação dos Entregadores')
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('###### Avaliação média por entregador')
        df1_avaliacao_media = df1.loc[:,['Delivery_person_ID','Delivery_person_Ratings']].groupby(['Delivery_person_ID']).mean().round(2).reset_index()
        df1_avaliacao_media.rename(columns={'Delivery_person_ID':'ID do Entregador', 'Delivery_person_Ratings':'Nota do Entregador'}, inplace=True)
        df1_avaliacao_media.index = range(1, len(df1_avaliacao_media) + 1)
        st.dataframe(df1_avaliacao_media)

    with col2:
        st.markdown('###### Avaliação média e desvio padrão por tráfego')
        df1_avaliacao_medio_desvio_trafego = avaliacao_medio_desvio(df1, cols=['Delivery_person_Ratings','Road_traffic_density'], group = ['Road_traffic_density'])
        df1_avaliacao_medio_desvio_trafego.rename(columns={'Road_traffic_density':'Densidade do Trânsito'}, inplace=True)
        df1_avaliacao_medio_desvio_trafego.index = range(1, len(df1_avaliacao_medio_desvio_trafego) + 1)
        st.dataframe(df1_avaliacao_medio_desvio_trafego)
        
    
        st.markdown('###### Avaliação média e desvio padrão por clima')
        df1_avaliacao_medio_desvio_clima = avaliacao_medio_desvio(df1, cols=['Delivery_person_Ratings','Weatherconditions'], group = ['Weatherconditions'])
        df1_avaliacao_medio_desvio_clima.rename(columns={'Weatherconditions':'Clima'},inplace=True)
        df1_avaliacao_medio_desvio_clima.index = range(1, len(df1_avaliacao_medio_desvio_clima) + 1)
        st.dataframe(df1_avaliacao_medio_desvio_clima)

  
    
with st.container():
    st.markdown("""---""")
    st.markdown('#### Velocidade de Entrega')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('###### Top 10 mais rápidos')
        df_top_10_rapidos = top_10_entregadores(df1, top_asc=True)
        st.dataframe(df_top_10_rapidos)
        
            
    with col2:
        st.markdown('###### Top 10 mais lentos')
        df_top_10_lentos = top_10_entregadores(df1, top_asc=False)
        st.dataframe(df_top_10_lentos)
    
    
