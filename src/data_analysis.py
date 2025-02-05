import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def basic_statistics(df):
    """Exibe estatísticas básicas dos dados."""
    print("📌 Primeiras linhas do dataset:")
    print(df.head(), "\n")

    print("📌 Informações gerais do dataset:")
    print(df.info(), "\n")

    print("📌 Estatísticas descritivas:")
    print(df.describe(), "\n")

def plot_satisfaction_distribution(df):
    """Plota a distribuição da satisfação dos clientes."""
    plt.figure(figsize=(8, 5))
    sns.countplot(x="csat_score", data=df, palette="viridis")
    plt.title("Distribuição da Satisfação dos Clientes")
    plt.xlabel("Nota de Satisfação")
    plt.ylabel("Quantidade")
    plt.show()
