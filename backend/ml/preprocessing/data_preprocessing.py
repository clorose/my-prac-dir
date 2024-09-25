import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

def preprocess_data(X, y, id_material, method='none'):
    preprocessing_methods = {
        'none': no_preprocessing,
        'delete': delete_missing,
        'mean': mean_imputation,
        'median': median_imputation,
        'mode': mode_imputation,
        'knn': knn_imputation
    }
    
    if method not in preprocessing_methods:
        raise ValueError(f"Invalid preprocessing method: {method}")
    
    return preprocessing_methods[method](X, y, id_material)

def no_preprocessing(X, y, id_material):
    return X, y, id_material

def delete_missing(X, y, id_material):
    # 결측치가 있는 행 삭제
    df = pd.concat([X, y, id_material], axis=1)
    df_cleaned = df.dropna()
    
    # 데이터 분리
    X_cleaned = df_cleaned[X.columns]
    y_cleaned = df_cleaned[y.name]
    id_material_cleaned = df_cleaned[id_material.columns]
    
    return X_cleaned, y_cleaned, id_material_cleaned

def mean_imputation(X, y, id_material):
    # 평균값으로 결측치 대체
    X_imputed = X.fillna(X.mean())
    
    # y와 id_material은 변경하지 않음
    return X_imputed, y, id_material

def median_imputation(X, y, id_material):
    # 중앙값으로 결측치 대체
    X_imputed = X.fillna(X.median())
    
    return X_imputed, y, id_material

def mode_imputation(X, y, id_material):
    # 최빈값으로 결측치 대체
    X_imputed = X.fillna(X.mode().iloc[0])
    
    return X_imputed, y, id_material

def knn_imputation(X, y, id_material):
    # KNN Imputer를 사용하여 결측치 대체
    imputer = KNNImputer(n_neighbors=5)
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns, index=X.index)
    
    return X_imputed, y, id_material

def print_data_ranges(X):
    for column in X.columns:
        print(f"{column}: {X[column].min()} - {X[column].max()}")

# 추가적인 전처리 함수
def scale_features(X):
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    return X_scaled

def remove_outliers(X, y, id_material, threshold=3):
    # Z-score 방법을 사용한 이상치 제거
    z_scores = np.abs((X - X.mean()) / X.std())
    X_cleaned = X[(z_scores < threshold).all(axis=1)]
    y_cleaned = y[X_cleaned.index]
    id_material_cleaned = id_material[X_cleaned.index]
    return X_cleaned, y_cleaned, id_material_cleaned

# 필요에 따라 추가 전처리 메서드를 구현할 수 있습니다.