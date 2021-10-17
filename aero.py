import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk

DATA_URL = "https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv"

@st.cache
def load_data():
    # importar o arquivo csv
    data = pd.read_csv(DATA_URL, index_col='codigo_ocorrencia')
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    data = data.rename(columns=columns)

    data.data = data.data + " " + data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    return data

#carregar os dados
df = load_data()
labels = df.classificacao.unique().tolist()

## SIDE BAR


# parâmetros e número de ocorrências

st.sidebar.header('Parâmetros')
info_sidebar = st.sidebar.empty() # place holder, para informações filtradas que só serão carregadas depois


#slider de seleção do ano
st.sidebar.subheader('Ano')
year_to_filter = st.sidebar.slider('Escolha o ano da análise', 2008,2018, 2010)

#checkbox da tabela
st.sidebar.subheader('Tabela')
tabela = st.sidebar.empty()


#multiselection com os labels únicos dos tipos de classificação
label_to_filter = st.sidebar.multiselect(label='Escolha a clssificação de ocorrência', options=labels, default=['ACIDENTE'])

filtered_df = df[ (df.data.dt.year == year_to_filter) & (df.classificacao.isin(label_to_filter)) ]

info_sidebar.info(f'{filtered_df.shape[0]} ocorrências selecionadas')

st.sidebar.markdown(f"""
A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes Aeronáuticos (CENIPA)***

""")



#MAIN
st.title('CENIPA - Acidentes Aeronáuticos')

st.markdown(f"""
Estão sendo exibidas as ocorrências classificadas como **{', '.join(label_to_filter)}** para o ano de **{year_to_filter}**

""")

#st.map(filtered_df)


# mapa
st.subheader("Mapa de ocorrências")
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=-22.96592,
        longitude=-43.17896,
        zoom=3,
        pitch=50
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=filtered_df,
            disk_resolution=12,
            radius=30000,
            get_position='[longitude,latitude]',
            get_fill_color='[255, 255, 255, 255]',
            get_line_color="[255, 255, 255]",
            auto_highlight=True,
            elevation_scale=1500,
            # elevation_range=[0, 3000],
            # get_elevation="norm_price",
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[longitude, latitude]',
            get_color='[255, 255, 255, 30]',
            get_radius=60000,
        ),
    ],
))

if tabela.checkbox('Mostrar tabela de dados'):
    st.write(filtered_df)



