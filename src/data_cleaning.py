import pandas as pd

def clean_data(df):
    """Realiza limpeza básica dos dados."""
    df = df.dropna()  # Remove valores nulos
    df.columns = df.columns.str.lower().str.replace(" ", "_")  # Formata os nomes das colunas
    return df

if __name__ == "__main__":
    df = pd.read_csv("../data/raw/Customer_support_data.csv")
    df_cleaned = clean_data(df)
    print(df_cleaned.info())  # Exibe informações dos dados limpos
