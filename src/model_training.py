import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import RandomOverSampler
import joblib

# 1️⃣ Carregar os dados
df = pd.read_csv("data/raw/Customer_support_data.csv")

# 2️⃣ Padronizar os nomes das colunas
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# 3️⃣ Remover colunas irrelevantes
df = df.drop(columns=["unique_id", "order_id", "order_date_time", "issue_reported_at", "survey_response_date"], errors='ignore')

# 4️⃣ Tratar valores ausentes
df = df.dropna()

# 5️⃣ Identificar todas as colunas categóricas
categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()

# Criar dicionário para armazenar os encoders
encoders = {}

# Converter todas as colunas categóricas usando LabelEncoder
for col in categorical_columns:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# 6️⃣ Definir as variáveis independentes (X) e a variável alvo (y)
X = df.drop(columns=["csat_score"])
y = df["csat_score"]

# 🔍 Verificar distribuição de classes antes do balanceamento
print("Distribuição das classes em y antes do balanceamento:")
print(y.value_counts())

# 7️⃣ Balancear as classes com RandomOverSampler
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)

# 🔍 Verificar a nova distribuição de classes
print("Distribuição das classes após o balanceamento:")
print(pd.Series(y_resampled).value_counts())

# 8️⃣ Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# 9️⃣ Criar e treinar um modelo de Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔟 Fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# 📊 Avaliar o desempenho do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo após melhorias: {accuracy:.2f}")
print("Relatório de Classificação:\n", classification_report(y_test, y_pred, zero_division=1))

# 💾 Salvar o modelo treinado
joblib.dump(model, "models/random_forest_model.pkl")
print("Modelo salvo em: models/random_forest_model.pkl")
