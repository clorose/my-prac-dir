# File: C:\_YHJ\fast\backend\ml\preprocessing\data_preprocessing.py
# Purpose: [Describe the purpose of this file]

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class ConsistentLabelEncoder:
    def __init__(self):
        self.encoders = {}

    def fit_transform(self, X):
        X_transformed = X.copy()
        for column in X.columns:
            if X[column].dtype == 'object':
                unique_values = X[column].unique()
                self.encoders[column] = {val: idx for idx, val in enumerate(unique_values)}
                X_transformed[column] = X[column].map(self.encoders[column])
        return X_transformed

    def inverse_transform(self, X):
        X_transformed = X.copy()
        for column in X.columns:
            if column in self.encoders:
                inverse_encoder = {idx: val for val, idx in self.encoders[column].items()}
                X_transformed[column] = X_transformed[column].map(inverse_encoder)
        return X_transformed

def apply_preprocessing_pipeline(X, y, id_material, preprocessing_methods):
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', 'passthrough', categorical_features)
        ])

    for method in preprocessing_methods:
        if method == 'standardization':
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(), numeric_features),
                    ('cat', 'passthrough', categorical_features)
                ])
        elif method == 'normalization':
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', MinMaxScaler(), numeric_features),
                    ('cat', 'passthrough', categorical_features)
                ])
        elif method == 'imputation':
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', SimpleImputer(strategy='mean'), numeric_features),
                    ('cat', SimpleImputer(strategy='most_frequent'), categorical_features)
                ])

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
    ])

    X_processed = pd.DataFrame(pipeline.fit_transform(X), columns=X.columns)
    
    label_encoder = ConsistentLabelEncoder()
    X_processed = label_encoder.fit_transform(X_processed)
    
    return X_processed, y, id_material

def print_data_ranges(X):
    for column in X.columns:
        print(f"{column}: {X[column].min()} - {X[column].max()}")

def check_negative_values(X):
    for column in X.columns:
        if (X[column] < 0).any():
            print(f"Negative values found in column: {column}")
        else:
            print(f"No negative values in column: {column}")

def essential_preprocessing(X, y, id_material):
    # Handle missing values
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns
    
    X[numeric_features] = X[numeric_features].fillna(X[numeric_features].mean())
    X[categorical_features] = X[categorical_features].fillna(X[categorical_features].mode().iloc[0])
    y = y.fillna(y.mode().iloc[0])
    id_material = id_material.fillna(id_material.mode().iloc[0])

    # Remove duplicates
    duplicates = X.duplicated()
    X = X[~duplicates]
    y = y[~duplicates]
    id_material = id_material[~duplicates]

    # Handle outliers (using IQR method)
    Q1 = X[numeric_features].quantile(0.25)
    Q3 = X[numeric_features].quantile(0.75)
    IQR = Q3 - Q1
    X = X[~((X[numeric_features] < (Q1 - 1.5 * IQR)) | (X[numeric_features] > (Q3 + 1.5 * IQR))).any(axis=1)]
    y = y[X.index]
    id_material = id_material[X.index]

    return X, y, id_material

def handle_missing_values(X, strategy='mean'):
    if strategy == 'mean':
        return X.fillna(X.mean())
    elif strategy == 'median':
        return X.fillna(X.median())
    elif strategy == 'mode':
        return X.fillna(X.mode().iloc[0])
    else:
        raise ValueError("Invalid strategy. Choose 'mean', 'median', or 'mode'.")

def remove_outliers(X, method='iqr', threshold=1.5):
    if method == 'iqr':
        Q1 = X.quantile(0.25)
        Q3 = X.quantile(0.75)
        IQR = Q3 - Q1
        return X[~((X < (Q1 - threshold * IQR)) | (X > (Q3 + threshold * IQR))).any(axis=1)]
    elif method == 'zscore':
        from scipy import stats
        return X[(np.abs(stats.zscore(X)) < threshold).all(axis=1)]
    else:
        raise ValueError("Invalid method. Choose 'iqr' or 'zscore'.")

def normalize_data(X, method='minmax'):
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError("Invalid method. Choose 'minmax' or 'standard'.")
    
    return pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

def encode_categorical_variables(X, method='label'):
    if method == 'label':
        le = LabelEncoder()
        for column in X.select_dtypes(include=['object']):
            X[column] = le.fit_transform(X[column].astype(str))
    elif method == 'onehot':
        X = pd.get_dummies(X)
    else:
        raise ValueError("Invalid method. Choose 'label' or 'onehot'.")
    
    return X

def feature_engineering(X):
    # Add your feature engineering logic here
    # For example:
    # X['new_feature'] = X['feature1'] * X['feature2']
    return X

def reduce_dimensionality(X, method='pca', n_components=0.95):
    if method == 'pca':
        from sklearn.decomposition import PCA
        pca = PCA(n_components=n_components)
        X_reduced = pca.fit_transform(X)
        return pd.DataFrame(X_reduced, index=X.index)
    else:
        raise ValueError("Invalid method. Only 'pca' is currently supported.")