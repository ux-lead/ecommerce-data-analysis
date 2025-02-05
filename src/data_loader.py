import pandas as pd

def load_data(filepath):
    """Carrega o dataset e retorna um DataFrame do pandas."""
    return pd.read_csv(filepath)

if __name__ == "__main__":
    df = load_data("../data/raw/Customer_support_data.csv")
    print(df.head())  # Exibe as primeiras linhas para verificação

