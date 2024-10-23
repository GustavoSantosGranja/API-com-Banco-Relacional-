#Conexão com o banco de dados e enviar os dados para o DASHBOARD

#pip install  mysql-connector-python

#Conexão
import mysql.connector
import pandas as pd

def conexao(query):
    conn = mysql.connector.connect(
        host = "127.0.0.1",
        port = "3306",
        user = "root",
        password = "senai@134",
        db = "bd_carro"
    )


    dataframe = pd.read_sql(query, conn )
    #executa a consulta SQL e armazena o resultado de um DATAFRAME

    conn.close()

    return dataframe