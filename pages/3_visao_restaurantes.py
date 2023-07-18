import pandas as pd
from datetime import datetime
import folium
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Restaurante', layout='wide')

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

    #Resetando index
    df1 = df1.reset_index( drop=True )
    
    return df1

# DESENVOLVIMENTO DOS DADOS PARA GRÁFICOS E TABELAS

def distancia_media(df1, figure):
    colunas = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
    df1['Distancia_media'] = df1.loc[:, colunas].apply(lambda row: haversine((row['Restaurant_latitude'], row['Restaurant_longitude']), (row['Delivery_location_latitude'], row['Delivery_location_longitude'])), axis=1)
    if figure == True:
        df1_distancia_media = df1.loc[:,['City','Distancia_media']].groupby(['City']).mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=df1_distancia_media['City'], values=df1_distancia_media['Distancia_media'], pull=[0,0.1,0])])
        return fig
    elif figure == False:
        distancia_media_val = np.round(df1['Distancia_media'].mean(), 2)
        return distancia_media_val
            

def entrega_festival_TempoMedio_desvio (df1, festival, calculo):
    df1_entrega_festival = df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']})
    df1_entrega_festival.columns = ['Tempo_medio','Tempo_desvio']
    df1_entrega_festival = df1_entrega_festival.reset_index()
    resultado = 0
    if calculo == 'tempo_medio':
        resultado = np.round(df1_entrega_festival.loc[df1_entrega_festival['Festival']==festival,['Tempo_medio']].sum(),2)
    elif calculo == 'desvio_padrao':
        resultado = np.round(df1_entrega_festival.loc[df1_entrega_festival['Festival']==festival,['Tempo_desvio']].sum(), 2)
    return resultado

def media_desvio_cidade(df1):
    df1_media_desvio_cidade = df1.loc[:,['Time_taken(min)','City']].groupby(['City']).agg(['mean', 'std'])
    df1_media_desvio_cidade.columns = ['Tempo_medio','Tempo_desvio']
    df1_media_desvio_cidade = df1_media_desvio_cidade.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df1_media_desvio_cidade['City'], y=df1_media_desvio_cidade['Tempo_medio'], error_y=dict(type='data', array=df1_media_desvio_cidade['Tempo_desvio'])))
    fig.update_layout(barmode='group')
    return fig

def media_desvio_pedido(df1):
    df1_media_desvio_pedido = df1.loc[:,['Time_taken(min)','City', 'Type_of_order']].groupby(['City','Type_of_order']).agg(['mean', 'std'])
    df1_media_desvio_pedido.columns = ['Tempo_medio','Tempo_desvio']
    df1_media_desvio_pedido = df1_media_desvio_pedido.reset_index()
    return df1_media_desvio_pedido

def media_desvio_trafego(df1):
    df1_media_desvio_trafego = df1.loc[:,['Time_taken(min)','City', 'Road_traffic_density']].groupby(['City','Road_traffic_density']).agg(['mean', 'std'])
    df1_media_desvio_trafego.columns = ['Tempo_medio','Tempo_desvio']
    df1_media_desvio_trafego = df1_media_desvio_trafego.reset_index()
    fig = px.sunburst(df1_media_desvio_trafego, path=['City','Road_traffic_density'], values='Tempo_medio', color='Tempo_desvio', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df1_media_desvio_trafego['Tempo_desvio']))
    return fig

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
date_slider = st.sidebar.slider('Qual o periodo?', value=datetime(2022,3,11), min_value=datetime(2022,2,11), max_value=datetime(2022,4,6), format='DD-MM-YYYY')
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
    st.header('Visão Geral dos Restaurantes')
    col1, col2, col3, col4, col5, col6 = st.columns(6)
      
        
    with col1:
        qtde_entregadores = df1['Delivery_person_ID'].nunique()
        col1.metric(' Entregadores Únicos', qtde_entregadores)
    
    with col2:
        distancia = distancia_media(df1, figure=False)
        col2.metric('Percurso médio (KM)', distancia)   
    
    with col3:
        tempo_medio_com_festival = entrega_festival_TempoMedio_desvio (df1, festival='Yes', calculo='tempo_medio')
        col3.metric('Tempo de Entrega c/ Festival', tempo_medio_com_festival)

    with col4:
        desvio_padrao_com_festival = entrega_festival_TempoMedio_desvio (df1, festival='Yes', calculo='desvio_padrao')
        col4.metric('Desvio Padrão c/ Festival', desvio_padrao_com_festival)
        
    with col5:
        tempo_medio_sem_festival = entrega_festival_TempoMedio_desvio (df1, festival='No', calculo='tempo_medio')
        col5.metric('Tempo de Entrega s/ Festival', tempo_medio_sem_festival)
        
    with col6:
        desvio_padrao_sem_festival = entrega_festival_TempoMedio_desvio (df1, festival='No', calculo='desvio_padrao')
        col6.metric('Desvio Padrão s/ Festival', desvio_padrao_sem_festival)
        
        
with st.container():
    st.markdown("""---""")
    st.header('Tempo Medio de entrega por cidade')
    col1, col2 = st.columns(2, gap='large')
    
    with col1:
        fig = media_desvio_cidade(df1)
        st.plotly_chart(fig)
    
    with col2:
        df1_media_desvio_pedido = media_desvio_pedido(df1)
        st.dataframe(df1_media_desvio_pedido)
    

with st.container():
    st.markdown("""---""")
    st.header('Distribuição do tempo')
    
    col1, col2 = st.columns(2, gap='large')
    with col1:  
        fig = distancia_media(df1, figure=True)
        st.plotly_chart(fig)


        
    with col2:
        fig = media_desvio_trafego(df1)
        st.plotly_chart(fig)
        
