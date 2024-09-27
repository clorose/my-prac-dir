import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, f1_score, roc_auc_score

class XGModel:
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
        self.target_column = 'Defect_Flag'

    def load_data_and_train_model(self, X, y, id_material, **model_params):
        try:
            self.X_processed = X
            self.y_processed = y
            self.id_material = id_material
            self.features = X.columns
            
            X_train, self.X_test, y_train, self.y_test, id_material_train, self.id_material_test = train_test_split(
                self.X_processed, self.y_processed, self.id_material, test_size=0.2, random_state=42)

            # 클래스 불균형 처리
            pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

            # 기본 모델 파라미터 설정
            default_params = {
                'n_estimators': 100,
                'max_depth': 3,
                'learning_rate': 0.1,
                'random_state': 42,
                'n_jobs': -1,
                'scale_pos_weight': pos_weight
            }

            # JSON에서 전달된 파라미터로 기본 파라미터 업데이트
            default_params.update(model_params)

            # 모델 생성 및 학습
            self.model = XGBClassifier(**default_params)
            self.model.fit(X_train, y_train)

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

    def get_feature_importance(self):
        importance = self.model.feature_importances_
        importance = 100.0 * (importance / importance.max())
        return dict(sorted(zip(self.features, importance), key=lambda x: x[1], reverse=True))

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