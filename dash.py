#pip install streamlit
#pip install streamlit_option_menu

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu 
from query import conexao

#*** Primeira Consulta / Atualizações de Dados ***
#consultar os dados
query = "SELECT * FROM tb_carros"

#Carregar os dados 
df = conexao(query)

# Botão para atualizar
if st.button("Atualizar Dados"):
    df = conexao(query)


# *** Estrutura lateral de filtros *****
st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada", # nome Seletor
                               options= df["marca"].unique(),
                               default= df["marca"].unique()
                               ) 

modelo = st.sidebar.multiselect("Marca Selecionado", # nome Seletor
                               options= df["modelo"].unique(),
                               default= df["modelo"].unique()
                               ) 

ano = st.sidebar.multiselect("Marca Selecionado", # nome Seletor
                               options= df["ano"].unique(),
                               default= df["ano"].unique()
                               ) 

valor = st.sidebar.multiselect("Marca Selecionado", # nome Seletor
                               options= df["valor"].unique(),
                               default= df["valor"].unique()
                               ) 

cor = st.sidebar.multiselect("Marca Selecionada", # nome Seletor
                               options= df["cor"].unique(),
                               default= df["cor"].unique()
                               ) 

numero_vendas = st.sidebar.multiselect("Marca Selecionada", # nome Seletor
                               options= df["numero_vendas"].unique(),
                               default= df["numero_vendas"].unique()
                               ) 

#aplicar filtros selecionados

df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas))
]

# ****** Exibir Valores Médios  - Estátistica

def Home():
    with st.expander("Valores"):#cria uma caixa expansiva com um titulo 
        mostrarDados = st.multiselect('Filter: ', df_selecionado.columns, default=[])
        #verifica se o usuario selecionou as colunas para exibir 
        if mostrarDados: 
            #exibe os dados filtrados pelas colunas selecionadas 
            st.write(df_selecionado[mostrarDados])

    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()

        total1, total2, total3 = st.columns(3, gap="large")

        with total1:
            st.info("Valor total de vendas dos Carros", icon='📌')
            st.metric(label="Total", value=f"{venda_total:,.0f}")

        with total2:
            st.info("Valor médio das vendas", icon='📌')
            st.metric(label='Média', value= f"{venda_media:,.0f}")

        with total3:
            st.info("Valor mediano dos carros", icon='📌')
            st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")

    #exibe um aviso se não houver dados disponiveis com filtros 
    else:
        st.warning("Nenhum dado disponivel com os filtros selecionados")
    
    #Insere uma linha divisoria
    st.markdown("""--------""")

#********** Graficos ****************

def graficos(df_selecionado):
    
    #verifica se o dataframe filtrado está vazio. Se estiver vazio exibe uma mensagem que não há dados para 
    # gerar gráficos e interronpe a função
    if df_selecionado.empty:
        st.warning("Nenhum dado disponivel para gerar gráficos")
        # Interrompe uma função, pq não há motivo para continuar executando se não tem dado
        return
    
    #Criação de graficos
    #4 Abas - Graficos de Barras, Linhas, Pizza e Dispersão

    graf1, graf2, graf3, graf4, graf6, graf7 = st.tabs(["Gráfico de Barras", "Grafico de Linhas", 
                                          "Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico de Área",
                                          "Gráfico de Dispersão 3D"])
    
    
    with graf1:
        st.write("Gráfico de Barras") #Titulo

        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by = "valor", ascending = False)
        #AGRUPA PELA MARCA E CONTA O NUMERO DE OCORRENCIAS PELA COLUNA VALOR E DEPOIS ORDENA O RESULTADO DE FORMA DECRESCENTE

        fig_valores = px.bar(investimento, #data frame que contem o valor das variaveis
                             x= investimento.index,
                             y= "valor",
                             orientation="v",
                             title="<b>Valores de Carros</b>",  #<b> antes e no final da frase para utilizar o negrito
                             color_discrete_sequence=["#0083b3"])
        
        #exibe e ajuda no ajuste fa tella
        st.plotly_chart(fig_valores, use_container_width=True)
                             
        
    with graf2:
        st.write("Gráfico de Linhas")
        dados = df_selecionado.groupby("marca").count()[["valor"]]

        fig_valores2 = px.line(dados, 
                           x= dados.index,
                           y= "valor",
                           title= "<b>Valores por Marca</b>",
                           color_discrete_sequence=["#0083b3"])
    
        st.plotly_chart(fig_valores2, use_container_width=True)


    with graf3:
        st.write("Gráfico de Pizza")
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]

        fig_valores3 = px.pie(dados2,
                              values= "valor",
                              names=dados2.index,
                              title="<b>Distribuição de Valores por Marca</b>")
        
        st.plotly_chart(fig_valores3, use_container_width=True)


    with graf4:
        st.write("Gráfico de Dispersão")
        dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])


        fig_valores4 = px.scatter(dados3,
                                  x="marca",
                                  y="value",
                                  color="variable",
                                  title="<b>Dipersão de Valores por Marca</b>")
        
        st.plotly_chart(fig_valores4, use_container_width=True)


    with graf6:
        st.write("Gráfico de Área")
        dados_area = df_selecionado.groupby("marca").sum()[["valor"]]

        fig_area = px.area(dados_area,
                       x=dados_area.index,
                       y="valor",
                       title="<b>Valores Acumulados por Marca</b>",
                       color_discrete_sequence=["#0083b3"])
    
        st.plotly_chart(fig_area, use_container_width=True)

    with graf7:
        st.write("Gráfico de Dispersão 3D")
    
        fig_3d = px.scatter_3d(df_selecionado, 
                           x='valor', 
                           y='ano', 
                           z='numero_vendas',
                           color='marca',  # Diferenciar por cor de acordo com a marca
                           title="<b>Dispersão 3D: Valor, Ano e Número de Vendas</b>",
                           labels={'valor': 'Valor', 'ano': 'Ano', 'numero_vendas': 'Nº de Vendas'})
    
        st.plotly_chart(fig_3d, use_container_width=True)

    #************** Barra de Progresso**************
def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 2000000
    percentual = round((valorAtual/objetivo * 100))
    

    if percentual> 100:
        st.subheader("Valores Atingidos!!!")
    else:
        st.write(f"Você tem {percentual}% de {objetivo}. Corre atrás!!!")
        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text="Alvo %")

#************** MENU LATERAL

def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title = "Menu", options=["Home", "Progresso"],
        icons=["house","eye"], menu_icon="cast",
        default_index=0)

    if selecionado == "Home":
        st.subheader(f"Página: {selecionado}")
        Home()
        graficos(df_selecionado)

    if selecionado == "Progresso":
        st.subheader(f"Página: {selecionado}")
        barraprogresso()
        graficos(df_selecionado)

# *********** Ajustar o CSS ***************


menuLateral()