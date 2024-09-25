import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, f1_score, roc_auc_score
from datetime import datetime
from ml.preprocessing.data_preprocessing import preprocess_data, print_data_ranges

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
        self.target_column = None

    def load_data_and_train_model(self, data_file_path, preprocess_method='none'):
        try:
            # 데이터 불러오기
            data = pd.read_csv(data_file_path)

            # Machine_ID와 Material_Type 열 저장
            self.id_material = data.iloc[:, :2]

            # 나머지 특성 선택
            self.features = data.columns[2:-1]
            target_column = 'Defect_Flag'  # 명시적으로 목표 변수 지정

            # 특성 행렬 (X)와 목표 변수 (y) 설정
            self.X = data[self.features]
            self.y = data[target_column]

            # 데이터 전처리
            self.X_processed, self.y_processed, self.id_material = preprocess_data(self.X, self.y, self.id_material, method=preprocess_method)
            
            # 데이터 분할
            X_train, self.X_test, y_train, self.y_test, id_material_train, self.id_material_test = train_test_split(
                self.X_processed, self.y_processed, self.id_material, test_size=0.2, random_state=42)

            # 클래스 불균형 처리
            pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

            # 모델 생성 및 학습 (파라미터 최적화)
            self.model = XGBClassifier(
                n_estimators=100,
                max_depth=3,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1,  # 모든 가용 코어 사용
                scale_pos_weight=pos_weight  # 클래스 불균형 처리
            )
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

    def get_feature_importance(self):
        importance = self.model.feature_importances_
        importance = 100.0 * (importance / importance.max())
        return dict(sorted(zip(self.features, importance), key=lambda x: x[1], reverse=True))

    def plot_3d_scatter(self):
        top_features = sorted(zip(self.features, self.model.feature_importances_), key=lambda x: x[1], reverse=True)[:3]
        top_feature_names = [f[0] for f in top_features]

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')

        scatter = ax.scatter(self.X_processed[top_feature_names[0]], 
                             self.X_processed[top_feature_names[1]], 
                             self.y_processed,
                             c=self.y_processed, 
                             cmap='viridis', 
                             alpha=0.6)

        ax.set_xlabel(top_feature_names[0])
        ax.set_ylabel(top_feature_names[1])
        ax.set_zlabel(self.target_column)
        ax.set_title('3D Scatter Plot of Top 3 Important Features\nColor indicates Target Variable')

        plt.colorbar(scatter)
        plt.tight_layout()
        plt.show()

    def save_processed_data_to_csv(self, output_path):
        try:
            # 전체 처리된 데이터를 DataFrame으로 변환
            processed_data = pd.concat([self.id_material, self.X_processed], axis=1)
            processed_data['actual_target'] = self.y_processed
            processed_data['predicted_target'] = self.predict(self.X_processed)

            # CSV 파일로 저장
            processed_data.to_csv(output_path, index=False)
            print(f"Processed data saved to {output_path}")
            print(f"Number of rows in processed data: {len(processed_data)}")
        except Exception as e:
            print(f"An error occurred while saving processed data to CSV: {e}")
            raise

def main():
    xg_model = XGModel()

    try:
        # 데이터 파일 경로 설정
        data_file_path = Path(__file__).parent.parent / 'data' / 'Machining_Factory_Data10000.csv'
        
        # 전처리 방법 ('none', 'delete', 'mean', 'median', 'mode', 'knn')
        preprocess_method = 'delete'
        print(f"preprocess method : {preprocess_method}")
        xg_model.load_data_and_train_model(data_file_path, preprocess_method)

        # 모델 성능 평가
        accuracy, f1, auc, report = xg_model.get_model_performance()
        print(f"Accuracy: {accuracy * 100:.2f}%")
        print(f"F1 Score: {f1:.4f}")
        print(f"AUC: {auc:.4f}\n")

        print("Classification Report:")
        print(classification_report(xg_model.y_test, xg_model.model.predict(xg_model.X_test), zero_division=1))

        # 특성 중요도 출력
        feature_importance = xg_model.get_feature_importance()
        print("\nFeature Importances:")
        for feature, importance in feature_importance.items():
            print(f"{feature}: {importance:.2f}%")

        # 처리된 데이터를 CSV 파일로 저장
        currentTime = datetime.now().strftime("%H%M%S")
        output_path = Path(__file__).parent / f"processed_data{currentTime}.csv"
        xg_model.save_processed_data_to_csv(output_path)

        # 데이터 범위 출력
        print_data_ranges(xg_model.X_processed)

        # 3D 스캐터 플롯 표시
        xg_model.plot_3d_scatter()

    except Exception as e:
        print(f"An error occurred in main execution: {e}")

if __name__ == "__main__":
    main()