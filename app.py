# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações iniciais da página
st.set_page_config(page_title="Visualização de Dados com Streamlit", layout="wide")

# Título da aplicação
st.title("Visualização de Dados Interativa")

# Carregamento de dados
st.sidebar.header("Configurações")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Leitura do arquivo CSV
    df = pd.read_csv(uploaded_file)

    # Exibição das primeiras linhas do DataFrame
    st.write("Dados Carregados:")
    st.write(df.head())

    # Opções de Filtragem de Dados
    st.sidebar.header("Filtragem de Dados")
    unique_values = {col: df[col].unique() for col in df.select_dtypes(include=['object']).columns}
    selected_filters = {}
    for col, values in unique_values.items():
        selected_value = st.sidebar.multiselect(f"Filtre por {col}", values, default=values)
        if selected_value:
            selected_filters[col] = selected_value
    
    if selected_filters:
        for col, values in selected_filters.items():
            df = df[df[col].isin(values)]

    # Exibição dos dados filtrados
    st.write("Dados Filtrados:")
    st.write(df.head())

    # Estatísticas Descritivas
    st.sidebar.header("Estatísticas Descritivas")
    show_statistics = st.sidebar.checkbox("Mostrar estatísticas descritivas")
    if show_statistics:
        st.subheader("Estatísticas Descritivas")
        st.write(df.describe(include='all'))

    # Seleção da coluna para análise
    st.sidebar.header("Análise de Dados")
    coluna = st.sidebar.selectbox("Escolha a coluna para análise", df.columns)

    # Gráfico de distribuição da coluna selecionada
    st.subheader(f"Distribuição da Coluna: {coluna}")
    fig, ax = plt.subplots()
    sns.histplot(df[coluna], kde=True, ax=ax)
    ax.set_title(f"Distribuição de {coluna}")
    st.pyplot(fig)

    # Gráfico de dispersão se houver mais de uma coluna
    if len(df.columns) > 1:
        st.sidebar.header("Gráfico de Dispersão")
        coluna_x = st.sidebar.selectbox("Escolha a coluna para o eixo X", df.columns, index=0)
        coluna_y = st.sidebar.selectbox("Escolha a coluna para o eixo Y", df.columns, index=1)

        st.subheader(f"Gráfico de Dispersão: {coluna_x} vs {coluna_y}")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=coluna_x, y=coluna_y, ax=ax)
        ax.set_title(f"Dispersão de {coluna_x} vs {coluna_y}")
        st.pyplot(fig)

    # Gráfico de Boxplot
    if len(df.columns) > 1:
        st.sidebar.header("Boxplot")
        coluna_box = st.sidebar.selectbox("Escolha a coluna para o Boxplot", df.columns, index=0)

        st.subheader(f"Boxplot da Coluna: {coluna_box}")
        fig, ax = plt.subplots()
        sns.boxplot(data=df, y=coluna_box, ax=ax)
        ax.set_title(f"Boxplot de {coluna_box}")
        st.pyplot(fig)

else:
    st.write("Por favor, carregue um arquivo CSV para começar.")

# Rodapé
st.sidebar.info("Desenvolvido com Streamlit")
