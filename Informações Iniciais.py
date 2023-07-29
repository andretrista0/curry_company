import streamlit as st
from PIL import Image

st.set_page_config(page_title="Informações Iniciais")

image = Image.open('logo.png')
st.sidebar.image(image, width=128)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")
st.write ('# Curry Company Growth Dashboard')

st.markdown(''' 
Growth Dashboard foi construído para acompanhar as métricas de crescimento da Empresa, dos Entregadores e Restaurente.
- Visão Empresa:
    - Visão Gerencial: Métricas gerais de comportamento
    - Visão Tática: Indicadores semanais de crescimento
    - Visão Geográfica: Insights de geolocalização
    
- Visão Entregadores:
    - Acompanhamento dos indicadores semanais de crescimento
    
- Visão Restaurente:
    - Indicadores semanais de crescimento dos restaurentes
''')
