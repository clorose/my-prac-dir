import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, f1_score, roc_auc_score
from ml.preprocessing.data_preprocessing import preprocess_data
from ml.utils.visualization import plot_3d_scatter

class KNNModel:
    def __init__(self):
        self.model = None
        self.X = None
        self.y = None
        self.X_test = None
        self.y_test = None
        self.features = None
        self.X_processed = None
        self.y_processed = None
        self.id_material = None
        self.id_material_test = None
        self.target_column = None

    def load_data_and_train_model(self, data_file_path, preprocess_method='none', n_neighbors=5):
        try:
            data = pd.read_csv(data_file_path)
            self.id_material = data.iloc[:, :2]
            self.features = data.columns[2:-1]
            target_column = 'Defect_Flag'
            self.X = data[self.features]
            self.y = data[target_column]
            
            self.X_processed, self.y_processed, self.id_material = preprocess_data(self.X, self.y, self.id_material, method=preprocess_method)
            
            X_train, self.X_test, y_train, self.y_test, id_material_train, self.id_material_test = train_test_split(
                self.X_processed, self.y_processed, self.id_material, test_size=0.2, random_state=42)

            self.model = KNeighborsClassifier(n_neighbors=n_neighbors, n_jobs=-1)
            self.model.fit(X_train, y_train)

            print(f"원본 데이터 shape: {data.shape}")
            print(f"전처리 후 데이터 shape: {self.X_processed.shape}")
            print(f"Number of samples in training set: {len(X_train)}")
            print(f"Number of samples in test set: {len(self.X_test)}")
            print(f"Class distribution in training set: {dict((k, int(v)) for k, v in y_train.value_counts().items())}")
            print(f"Class distribution in test set: {dict((k, int(v)) for k, v in self.y_test.value_counts().items())}")
        except Exception as e:
            print(f"An error occurred while loading data and training model: {e}")
            raise

    def predict(self, input_data):
        return self.model.predict(input_data)

    def get_model_performance(self):
        try:
            y_pred = self.model.predict(self.X_test)
            y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
            
            accuracy = accuracy_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred)
            auc = roc_auc_score(self.y_test, y_pred_proba)
            
            report = classification_report(self.y_test, y_pred, output_dict=True, zero_division=1)
            
            return accuracy, f1, auc, report
        except Exception as e:
            print(f"An error occurred while getting model performance: {e}")
            raise

    def plot_3d_scatter(self):
        plot_3d_scatter(self.X_processed, self.y_processed, self.features)

    def save_processed_data_to_csv(self, output_path):
        try:
            processed_data = pd.concat([self.id_material, self.X_processed], axis=1)
            processed_data['actual_target'] = self.y_processed
            processed_data['predicted_target'] = self.predict(self.X_processed)

            processed_data.to_csv(output_path, index=False)
            print(f"Processed data saved to {output_path}")
            print(f"Number of rows in processed data: {len(processed_data)}")
        except Exception as e:
            print(f"An error occurred while saving processed data to CSV: {e}")
            raise