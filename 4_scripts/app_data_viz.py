import streamlit as st
import pandas as pd
import plotly.express as px

st.write('**APP Futebol**')
st.sidebar.header('Escolha dos times')

df = pd.read_csv('../1_bases_tratadas/dadostratados.csv', 
                sep=';', encoding='utf-8')
times = df['home_team_name'].drop_duplicates()
time_escolhido = st.sidebar.selectbox('Selecione um time', times)

df2 = df.loc[df['home_team_name']==time_escolhido]
st.write(f'Time escolhido:{time_escolhido}')
st.write('Pontos por jogo')
fig = px.box(df2, x='home_ppg')

col1, col2, col3 = st.columns(3)
col1.metric("Gols médio",
            value=df2.home_team_goal_count.mean().round(2))
col2.metric("Escanteios médios",
            value=df2.home_team_corner_count.mean().round(2))
col3.metric("Pontos médios",
            value=df2.home_ppg.mean().round(2))
st.plotly_chart(fig)

