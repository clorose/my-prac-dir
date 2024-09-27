import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler
import json

class ConsistentLabelEncoder:
    def __init__(self, mapping_file=os.path.join(os.path.dirname(__file__), '..', 'label_mapping.json')):
        self.mapping_file = mapping_file
        self.encoders = {}
        self.load_mapping()

    def load_mapping(self):
        try:
            with open(self.mapping_file, 'r') as f:
                self.encoders = json.load(f)
        except FileNotFoundError:
            self.encoders = {}

    def save_mapping(self):
        with open(self.mapping_file, 'w') as f:
            json.dump(self.encoders, f, indent=4)

    def fit_transform(self, X):
        for column in X.columns:
            # 결측치 처리: 모든 컬럼에서 결측치를 'Missing'으로 대체하고 문자열로 변환
            X[column] = X[column].fillna('Missing').astype(str)
            if column not in self.encoders or not self.encoders[column]:
                unique_values = X[column].unique()
                # 매핑 생성: 고유한 값들에 인덱스 할당
                mapping = {value: index for index, value in enumerate(unique_values)}
                self.encoders[column] = mapping
            mapping = self.encoders[column]
            X[column] = X[column].map(mapping)
            # 매핑되지 않은 값(NaN)을 'Missing'의 매핑 값으로 대체
            if 'Missing' in mapping:
                missing_value = mapping['Missing']
                X[column] = X[column].fillna(missing_value)
            else:
                # 'Missing'이 매핑에 없을 경우, 매핑에 추가
                missing_value = len(mapping)
                mapping['Missing'] = missing_value
                X[column] = X[column].fillna(missing_value)
            X[column] = X[column].astype(int)
        self.save_mapping()
        return X

    def transform(self, X):
        for column in X.columns:
            # 결측치 처리: 모든 컬럼에서 결측치를 'Missing'으로 대체하고 문자열로 변환
            X[column] = X[column].fillna('Missing').astype(str)
            if column in self.encoders:
                mapping = self.encoders[column]
                X[column] = X[column].map(mapping)
                # 매핑되지 않은 값(NaN)을 'Missing'의 매핑 값으로 대체
                if 'Missing' in mapping:
                    missing_value = mapping['Missing']
                    X[column] = X[column].fillna(missing_value)
                else:
                    # 'Missing'이 매핑에 없을 경우, 매핑에 추가
                    missing_value = len(mapping)
                    mapping['Missing'] = missing_value
                    X[column] = X[column].fillna(missing_value)
                X[column] = X[column].astype(int)
            else:
                print(f"Warning: {column} not found in the encoder mapping. Skipping this column.")
        return X

    def inverse_transform(self, X):
        for column in X.columns:
            if column in self.encoders:
                inverse_mapping = {v: k for k, v in self.encoders[column].items()}
                X[column] = X[column].map(inverse_mapping)
        return X


def essential_preprocessing(X, y, id_material):
    # 범주형 변수 인코딩 전에 결측치 처리
    X = X.fillna('Missing').astype(str)
    # 범주형 변수 인코딩
    encoder = ConsistentLabelEncoder()
    X = encoder.fit_transform(X)
    return X, y, id_material

def preprocess_data(X, y, id_material, method):
    preprocessing_methods = {
        'delete': delete_missing,
        'mean': mean_imputation,
        'median': median_imputation,
        'mode': mode_imputation,
        'knn': knn_imputation,
        'scale': scale_features,
        'remove_outliers': remove_outliers,
        'log_transform': log_transform
    }

    if method not in preprocessing_methods:
        raise ValueError(f"Invalid preprocessing method: {method}")

    return preprocessing_methods[method](X, y, id_material)

def delete_missing(X, y, id_material):
    df = pd.concat([X, y, id_material], axis=1)
    df_cleaned = df.dropna()
    X_cleaned = df_cleaned[X.columns]
    y_cleaned = df_cleaned[y.name]
    id_material_cleaned = df_cleaned[id_material.columns]
    return X_cleaned, y_cleaned, id_material_cleaned

def mean_imputation(X, y, id_material):
    X_imputed = X.copy()
    imputer = SimpleImputer(strategy='mean')
    X_imputed = pd.DataFrame(imputer.fit_transform(X_imputed), columns=X.columns, index=X.index)
    return X_imputed, y, id_material

def median_imputation(X, y, id_material):
    X_imputed = X.copy()
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X_imputed), columns=X.columns, index=X.index)
    return X_imputed, y, id_material

def mode_imputation(X, y, id_material):
    X_imputed = X.copy()
    imputer = SimpleImputer(strategy='most_frequent')
    X_imputed = pd.DataFrame(imputer.fit_transform(X_imputed), columns=X.columns, index=X.index)
    return X_imputed, y, id_material

def knn_imputation(X, y, id_material):
    imputer = KNNImputer(n_neighbors=5)
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns, index=X.index)
    return X_imputed, y, id_material

def scale_features(X, y, id_material):
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    return X_scaled, y, id_material

def remove_outliers(X, y, id_material, threshold=3):
    z_scores = np.abs((X - X.mean()) / X.std())
    mask = (z_scores < threshold).all(axis=1)
    return X[mask], y[mask], id_material[mask]

def log_transform(X, y, id_material):
    X_log = X.apply(lambda x: np.log1p(x) if (x > 0).all() else x)
    return X_log, y, id_material

def print_data_ranges(X):
    for column in X.columns:
        print(f"{column}: {X[column].min()} - {X[column].max()}")

def apply_preprocessing_pipeline(X, y, id_material, methods):
    # 'none'이 전처리 방법에 포함되어 있으면 모든 전처리를 건너뜁니다.
    if 'none' in methods:
        # 범주형 변수 인코딩은 모델 훈련을 위해 필요하므로 수행
        X, y, id_material = essential_preprocessing(X, y, id_material)
        return X, y, id_material

    # 필수 전처리 적용
    X, y, id_material = essential_preprocessing(X, y, id_material)

    # 사용자 선택 전처리 적용
    for method in methods:
        X, y, id_material = preprocess_data(X, y, id_material, method)

    return X, y, id_material

def check_negative_values(X):
    for column in X.columns:
        if (X[column] < 0).any():
            print(f"Negative values found in column: {column}")
        else:
            print(f"No negative values in column: {column}")
