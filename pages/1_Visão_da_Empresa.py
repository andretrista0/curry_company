import pandas as pd
import folium
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from datetime import datetime

st.set_page_config(page_title='Visão da Empresa', layout='wide')

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
    df1['Order_Date'] = pd.datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['Order_Date'] = pd.datetime(df1['Order_Date'], format='%H:%M:%S')
    df1['Time_Order_picked'] = pd.datetime(df1['Time_Order_picked'], format='%H:%M:%S')
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # Removendo parte do texto '(min) ' da coluna Time_taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    #Resetando index
    df1 = df1.reset_index( drop=True )
    
    return df1

# DESENVOLVIMENTO DOS DADOS PARA GRÁFICOS E TABELAS

def pedidos_dia(df1):
    df1_id_dia = df1.loc[:,['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
    fig = px.bar(df1_id_dia, x='Order_Date', y='ID', labels={'Order_Date':'Data do Pedido','ID':'Quantidade de Pedidos' })
    return fig

def pedidos_trafego(df1):
    df1_id_trafego = df1.loc[:,['ID', 'Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
    df1_id_trafego['Porcentagem'] = (df1_id_trafego['ID']*100) / sum(df1_id_trafego['ID'])
    fig = px.pie (df1_id_trafego, values='Porcentagem', names='Road_traffic_density', labels={'Road_traffic_density':'Densidade do Trânsito'})
    return fig

def pedidos_cidade_trafego(df1):
    df1_id_cidade_trafego = df1.loc[:,['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.bar(df1_id_cidade_trafego, x='City', y='ID', color='Road_traffic_density', barmode='group', labels={'Road_traffic_density':'Densidade do Trânsito', 'City':'Cidade','ID':'Quantidade de Pedidos'})
    return fig

def pedidos_semana(df1):
    df1['Order_Week'] = df1['Order_Date'].dt.strftime('%U')
    df1_id_dia_semana = df1.loc[:,['ID', 'Order_Week']].groupby(['Order_Week']).count().reset_index()
    fig = px.line(df1_id_dia_semana, x='Order_Week', y='ID', labels={'Order_Week':'Semana do Pedido','ID':'Quantidade de Pedidos'})
    return fig

def pedidos_entregador_semana(df1):
    df_pedido_semana = df1.loc[:,['ID', 'Order_Week']].groupby(['Order_Week']).count().reset_index()
    df_entregador_semana = df1.loc[:,['Delivery_person_ID', 'Order_Week']].groupby(['Order_Week']).nunique().reset_index()
    df_pedido_entregador_semana = pd.merge(df_pedido_semana, df_entregador_semana, how='inner')
    df_pedido_entregador_semana['Pedido_por_Entregador'] = df_pedido_entregador_semana['ID'] / df_pedido_entregador_semana['Delivery_person_ID']
    fig = px.line(df_pedido_entregador_semana, x='Order_Week', y='Pedido_por_Entregador', labels={'Order_Week':'Semana do Pedido','Pedido_por_Entregador':'Quantidade de Pedidos por Entregador'})
    return fig

def mapa_cidades(df1):
    df1_cidade_localizacao_trafego = df1.loc[:,['City', 'Delivery_location_latitude', 'Delivery_location_longitude', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    mapa = folium.Map( zoom_start=11 )

    for i , localizacao in df1_cidade_localizacao_trafego.iterrows():
      folium.Marker([localizacao['Delivery_location_latitude'], localizacao['Delivery_location_longitude']], popup=localizacao[['City', 'Road_traffic_density']]).add_to(mapa)
    return mapa

    
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

st.header('Visão da Empresa')

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        st.markdown('#### Pedidos por dia') 
        fig = pedidos_dia(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('#### Pedidos: tráfego') 
            fig = pedidos_trafego(df1)
            st.plotly_chart(fig, use_container_width=True)
         
        with col2:
            st.markdown('#### Pedidos: cidade e tráfego') 
            fig = pedidos_cidade_trafego(df1)
            st.plotly_chart(fig, use_container_width=True)
  
    
with tab2:
    st.markdown('#### Pedidos por semana')
    fig = pedidos_semana(df1)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('#### Pedidos por entregador por semana')
    fig = pedidos_entregador_semana(df1)
    st.plotly_chart(fig, use_container_width=True)
    
    
with tab3:
    st.markdown('#### Mapa das cidades')
    mapa = mapa_cidades(df1)
    folium_static(mapa, width=750, height=450)

