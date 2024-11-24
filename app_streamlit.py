import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import sqlite3
from sqlalchemy import create_engine 

# Configuração da aplicação
st.set_page_config(page_title="Análise Interativa", layout="wide")

# Função para carregar dados da API Flask
@st.cache_data
def carregar_dados(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Erro ao carregar os dados da API.")
        return pd.DataFrame()

# URL da API Flask
api_url = "http://127.0.0.1:5000/dados"

# Carregar os dados
dados = carregar_dados(api_url)

if dados.empty:
    st.stop()

# Interface do Streamlit
st.title("Análise Interativa de Dados")
st.sidebar.header("Configurações")

variavel = st.sidebar.selectbox("Selecione a variável para análise:", dados.columns)
tipo_analise = st.sidebar.radio("Tipo de Análise:", ["Univariada", "Multivariada"])

# Exibição de estatísticas
if variavel:
    media = dados[variavel].mean().round(2)
    mediana = dados[variavel].median().round(2)
    desvio = dados[variavel].std().round(2)

    st.write(f"**Média:** {media}")
    st.write(f"**Mediana:** {mediana}")
    st.write(f"**Desvio Padrão:** {desvio}")

# Análise Univariada
if tipo_analise == "Univariada":
    st.subheader(f"Análise Univariada - {variavel}")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Histograma**")
        fig = px.histogram(dados, x=variavel)
        st.plotly_chart(fig, use_container_width=True)

        st.write("**Boxplot**")
        fig = px.box(dados, y=variavel)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("**Gráfico de Barras**")
        fig = px.bar(dados, x=variavel)
        st.plotly_chart(fig, use_container_width=True)

# Análise Multivariada
elif tipo_analise == "Multivariada":
    variavel_color = st.sidebar.selectbox("Selecione a variável de cor:", dados.columns)
    st.subheader(f"Análise Multivariada: {variavel} vs {variavel_color}")

    fig = px.scatter(dados, x=variavel, y=variavel_color, color=variavel_color)
    st.plotly_chart(fig, use_container_width=True)
