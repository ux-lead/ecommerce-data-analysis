def plot_satisfaction_distribution(df):
    """
    Plota a distribuição da satisfação dos clientes.

    Parâmetros:
    df (pandas.DataFrame): Um DataFrame contendo os dados de satisfação dos clientes.
        O DataFrame deve ter uma coluna chamada 'satisfaction_rating' que representa a nota de satisfação dos clientes.

    Retorna:
    None

    Efeitos colaterais:
    Exibe um gráfico de barras usando a biblioteca seaborn, mostrando a distribuição da satisfação dos clientes.
    """
    plt.figure(figsize=(8, 5))
    sns.countplot(x="satisfaction_rating", data=df, palette="viridis")
    plt.title("Distribuição da Satisfação dos Clientes")
    plt.xlabel("Nota de Satisfação")
    plt.ylabel("Quantidade")
    plt.show()
