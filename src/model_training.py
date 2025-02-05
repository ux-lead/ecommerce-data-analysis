import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1️⃣ Carregar os dados
df = pd.read_csv("data/raw/Customer_support_data.csv")

# 2️⃣ Padronizar os nomes das colunas
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# 3️⃣ Remover colunas irrelevantes
df = df.drop(columns=["unique_id", "order_id", "order_date_time", "issue_reported_at", "survey_response_date"])

# 4️⃣ Tratar valores ausentes
df = df.dropna()

# 5️⃣ Converter variáveis categóricas em números
categorical_columns = ["channel_name", "product_category", "agent_name", "supervisor", "manager"]
encoders = {}

for col in categorical_columns:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# 6️⃣ Definir as variáveis independentes (X) e a variável alvo (y)
X = df.drop(columns=["csat_score"])
y = df["csat_score"]

# 7️⃣ Dividir os dados em treino e teste (80% treino, 20% teste)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 8️⃣ Criar e treinar um modelo de Regressão Logística
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 9️⃣ Fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# 🔟 Avaliar o desempenho do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy:.2f}")
print("Relatório de Classificação:\n", classification_report(y_test, y_pred))

# 🔥 Salvar o modelo treinado para uso posterior
import joblib
joblib.dump(model, "models/logistic_regression_model.pkl")

print("Modelo salvo em: models/logistic_regression_model.pkl")
