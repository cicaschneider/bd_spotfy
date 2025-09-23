import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# -------------------
# 1. Carregar e processar dados
# -------------------
df = pd.read_csv('Spotify_Churn.csv')

# Remover coluna irrelevante
if 'user_id' in df.columns:
    df = df.drop(columns=['user_id'])

# Renomear coluna alvo
if 'is_churned' in df.columns:
    df.rename(columns={'is_churned': 'is_churn'}, inplace=True)

# Preencher valores ausentes sem warnings do pandas 3.x
for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:
        df[col] = df[col].fillna(df[col].median())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])

# Converter target para numérico
le = LabelEncoder()
df['is_churn'] = le.fit_transform(df['is_churn'])

# One-hot encoding para colunas categóricas
categorical_cols = ['gender', 'country', 'subscription_type', 'device_type']
df = pd.get_dummies(df, columns=categorical_cols)

# Normalização dos numéricos
numerical_cols = ['age', 'listening_time', 'songs_played_per_day', 'skip_rate', 'ads_listened_per_week']
scaler = MinMaxScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# Criar dataframe de casos
cases = df.copy()

# -------------------
# 2. Funções RBC
# -------------------
def euclidean_distance(case1, case2):
    return np.sqrt(np.sum((case1 - case2) ** 2))

def retrieve_similar_cases(new_case, k=5):
    distances = []
    for i, case in cases.iterrows():
        dist = euclidean_distance(new_case.values, case.drop('is_churn').values)
        distances.append((i, dist))
    distances.sort(key=lambda x: x[1])
    indices = [i for i, _ in distances[:k]]
    return cases.iloc[indices]
