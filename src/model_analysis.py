import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Carregar o modelo treinado
model = joblib.load("models/random_forest_model.pkl")

# Carregar os dados originais para garantir que as colunas correspondam ao modelo treinado
df = pd.read_csv("data/raw/Customer_support_data.csv")
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# Remover a coluna de destino para garantir que X contenha apenas features
if "csat_score" in df.columns:
    df = df.drop(columns=["csat_score"])

# Ajustar para usar apenas as colunas que foram usadas no treinamento
feature_names = model.feature_names_in_  # Obtém os nomes das features usadas no treinamento
df = df[feature_names]  # Seleciona apenas as colunas que foram usadas no modelo

# Obter a importância das variáveis
feature_importance = model.feature_importances_
features = df.columns  # Agora garantimos que features e importance tenham o mesmo tamanho

# Criar gráfico
plt.figure(figsize=(12, 6))
plt.barh(features, feature_importance, color="skyblue")
plt.xlabel("Importância")
plt.ylabel("Variáveis")
plt.title("Importância das Variáveis no Modelo")
plt.show()
