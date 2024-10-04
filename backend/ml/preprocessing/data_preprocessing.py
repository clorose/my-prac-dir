# ml\preprocessing\data_preprocessing.py

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
        X_encoded = X.copy()
        for column in X.columns:
            if X[column].dtype == 'object':  # 문자열 데이터인 경우
                if column not in self.encoders or not self.encoders[column]:
                    unique_values = X[column].dropna().unique()
                    mapping = {value: index for index, value in enumerate(unique_values)}
                    self.encoders[column] = mapping
                mapping = self.encoders[column]
                X_encoded[column] = X_encoded[column].map(mapping)
            else:  # 숫자 데이터인 경우
                X_encoded[column] = pd.to_numeric(X_encoded[column], errors='coerce')
        self.save_mapping()
        return X_encoded

    def transform(self, X):
        X_encoded = X.copy()
        for column in X.columns:
            if column in self.encoders:
                mapping = self.encoders[column]
                X_encoded[column] = X_encoded[column].map(mapping)
            else:
                X_encoded[column] = pd.to_numeric(X_encoded[column], errors='coerce')
        return X_encoded

    def inverse_transform(self, X):
        X_decoded = X.copy()
        for column in X.columns:
            if column in self.encoders:
                inverse_mapping = {v: k for k, v in self.encoders[column].items()}
                X_decoded[column] = X_decoded[column].map(lambda x: inverse_mapping.get(x, np.nan))
        return X_decoded

def essential_preprocessing(X, y, id_material):
    # 범주형 변수 인코딩
    encoder = ConsistentLabelEncoder()
    X_encoded = encoder.fit_transform(X)
    
    # y를 숫자로 변환
    y = pd.to_numeric(y, errors='coerce')
    
    return X_encoded, y, id_material

def apply_preprocessing_pipeline(X, y, id_material, methods):
    preprocessing_methods = {
        'none': no_preprocessing,
        'delete': delete_missing,
        'mean': mean_imputation,
        'median': median_imputation,
        'mode': mode_imputation,
        'knn': knn_imputation,
        'scale': scale_features,
        'remove_outliers': remove_outliers,
        'log_transform': log_transform
    }

    for method in methods:
        if method not in preprocessing_methods:
            raise ValueError(f"Invalid preprocessing method: {method}")
        X, y, id_material = preprocessing_methods[method](X, y, id_material)

    return X, y, id_material

def no_preprocessing(X, y, id_material):
    return X, y, id_material

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
        if pd.api.types.is_numeric_dtype(X[column]):
            print(f"{column}: {X[column].min()} - {X[column].max()}")
        else:
            print(f"{column}: non-numeric data")

def check_negative_values(X):
    for column in X.columns:
        if pd.api.types.is_numeric_dtype(X[column]):
            if (X[column] < 0).any():
                print(f"Negative values found in column: {column}")
            else:
                print(f"No negative values in column: {column}")
        else:
            print(f"Skipping non-numeric column: {column}")