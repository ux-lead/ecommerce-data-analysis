import joblib
import numpy as np
import pandas as pd

# Carregar o modelo treinado
model = joblib.load("models/random_forest_model.pkl")

# Carregar os nomes das colunas usadas no treinamento
df = pd.read_csv("data/raw/Customer_support_data.csv")
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# Obter as colunas usadas no treinamento
feature_names = model.feature_names_in_

# Criar um novo atendimento fictício com os valores corretos (ajustar para 19 colunas)
novo_atendimento = pd.DataFrame(np.array([[1, 3, 2, "positive", "responded", "New York", 1, 500, 900, 2, 4, 1, "junior", "day"]]), columns=feature_names)

# Converter colunas categóricas para o mesmo formato do modelo (Label Encoding)
categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()
encoders = joblib.load("models/encoders.pkl")  # Supondo que os encoders foram salvos

for col in categorical_columns:
    if col in novo_atendimento.columns and col in encoders:
        novo_atendimento[col] = encoders[col].transform(novo_atendimento[col])

# Fazer a previsão
satisfacao_prevista = model.predict(novo_atendimento)
print(f"Satisfação prevista: {satisfacao_prevista[0]}")
