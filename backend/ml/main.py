import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import json
import argparse
from datetime import datetime
import pandas as pd
import numpy as np
import time  # 시간 측정을 위해 추가
from sklearn.metrics import classification_report
from ml.models.xg_model import XGModel
from ml.models.knn_model import KNNModel
from ml.models.rf_model import RFModel
from ml.preprocessing.data_preprocessing import apply_preprocessing_pipeline, print_data_ranges, ConsistentLabelEncoder, check_negative_values
from ml.utils.visualization import visualize_data  # 수정된 visualization.py 임포트

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def load_model_class(model_name):
    if model_name.lower() == 'xg':
        return XGModel
    elif model_name.lower() == 'knn':
        return KNNModel
    elif model_name.lower() == 'rf':
        return RFModel
    else:
        raise ValueError(f"Unknown model: {model_name}")

def run_model(model_config, data_file_path, preprocess_methods):
    model_class = load_model_class(model_config['name'])
    model = model_class()
    try:
        print(f"Model: {model_class.__name__}")
        print(f"Preprocess methods: {', '.join(preprocess_methods)}")
        
        # 시작 시간 기록
        start_time = time.time()
        
        # 데이터 로드
        data = pd.read_csv(data_file_path)
        print(f"Original data shape: {data.shape}")
        print(f"Columns in the data: {data.columns.tolist()}")

        # ID와 Material Type 분리
        id_material_columns = ['Timestamp', 'Machine_ID', 'Material_Type']
        id_material = data[id_material_columns]

        # 특성과 타겟 분리
        target_column = 'Quality_Result'
        features = [col for col in data.columns if col not in id_material_columns + [target_column, 'Defect_Type']]
        X = data[features].copy()

        # NaN 값 처리 및 안전한 타입 변환
        y = data[target_column]
        y = y.apply(lambda x: int(x) if pd.notnull(x) and np.isfinite(x) else np.nan)

        print(f"X shape before preprocessing: {X.shape}")
        print(f"y shape before preprocessing: {y.shape}")

        # y의 클래스 분포 확인
        print("Class distribution in y before preprocessing:")
        print(y.value_counts())

        # 전처리 파이프라인 적용
        X_processed, y_processed, id_material_processed = apply_preprocessing_pipeline(X, y, id_material, preprocess_methods)

        print(f"X shape after preprocessing: {X_processed.shape}")
        print(f"y shape after preprocessing: {y_processed.shape}")

        # y의 클래스 분포 확인 (전처리 후)
        print("Class distribution in y after preprocessing:")
        print(y_processed.value_counts())

        # 음수 값 확인
        check_negative_values(X_processed)

        # 타겟 변수의 결측치 제거
        valid_indices = y_processed.notnull()
        X_processed = X_processed[valid_indices]
        y_processed = y_processed[valid_indices]
        id_material_processed = id_material_processed[valid_indices]

        # 모델 훈련
        model.load_data_and_train_model(X_processed, y_processed, id_material_processed, **model_config.get('params', {}))

        # 종료 시간 기록
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total time taken for preprocessing and model training: {elapsed_time:.2f} seconds")

        # 모델 성능 평가
        accuracy, f1, auc, report = model.get_model_performance()
        print(f"Accuracy: {accuracy * 100:.2f}%")
        print(f"F1 Score: {f1:.4f}")
        print(f"AUC: {auc:.4f}\n")

        print("Classification Report:")
        print(classification_report(model.y_test, model.model.predict(model.X_test), zero_division=1))

        # 특성 중요도 추출
        if hasattr(model, 'get_feature_importance'):
            feature_importance_dict = model.get_feature_importance()
            features = list(feature_importance_dict.keys())
            feature_importances = list(feature_importance_dict.values())
            print("\nFeature Importances:")
            for feature, importance in feature_importance_dict.items():
                print(f"{feature}: {importance:.2f}%")
        else:
            feature_importances = None
            features = X_processed.columns.tolist()

        # 결과 저장
        currentTime = datetime.now().strftime("%H%M%S")
        output_path = Path(__file__).parent / 'output' / f"processed_data_{model_class.__name__}_{currentTime}.csv"
        save_results(model, X_processed, y_processed, id_material_processed, output_path)

        print_data_ranges(X_processed)

        # 시각화 함수 호출
        visualize_data(X_processed, y_processed, features, feature_importances)
    
    except Exception as e:
        print(f"An error occurred in model execution: {e}")
        import traceback
        traceback.print_exc()

def save_results(model, X_processed, y_processed, id_material_processed, output_path):
    # 인코딩된 값을 원래 값으로 복원
    encoder = ConsistentLabelEncoder()
    X_original = X_processed.copy()
    X_original = encoder.inverse_transform(X_original)

    # 결과 데이터 프레임 생성
    results = pd.concat([id_material_processed.reset_index(drop=True), X_original.reset_index(drop=True)], axis=1)
    results['actual_target'] = y_processed.reset_index(drop=True)
    results['predicted_target'] = model.predict(X_processed)

    # CSV로 저장
    results.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")
    print(f"Number of rows in processed data: {len(results)}")

def select_preprocess_methods(config):
    print("\nAvailable preprocessing methods:")
    for method in config['preprocess_methods']:
        print(f"- {method}")
    
    selected_methods = []
    while True:
        method = input("Enter a preprocessing method (or 'done' to finish): ").lower()
        if method == 'done':
            break
        if method in config['preprocess_methods']:
            if method not in selected_methods:
                selected_methods.append(method)
            else:
                print(f"'{method}' is already selected.")
        else:
            print(f"Invalid preprocessing method. Please choose from {', '.join(config['preprocess_methods'])}.")

    return selected_methods

def main():
    config = load_config()
    parser = argparse.ArgumentParser(description="Run machine learning models with preprocessing.")
    parser.add_argument('--model', type=str, choices=[model['name'] for model in config['models']], help="Select the model to run")
    parser.add_argument('--preprocess', type=str, nargs='+', choices=config['preprocess_methods'], help="Select the preprocessing methods")
    args = parser.parse_args()

    data_file_path = Path(__file__).parent / 'data' / 'data_09262024_120358.csv'

    if args.model and args.preprocess:
        model_config = next(model for model in config['models'] if model['name'] == args.model)
        preprocess_methods = args.preprocess
        print(f"Using model: {args.model}")
        print(f"Using preprocessing methods: {', '.join(preprocess_methods)}")
        run_model(model_config, data_file_path, preprocess_methods)
    else:
        while True:
            print("\nAvailable models:")
            for model in config['models']:
                print(f"- {model['name']}")
            
            model_name = input("Enter the name of the model you want to run (or 'q' to quit): ")
            if model_name.lower() == 'q':
                break

            model_config = next((model for model in config['models'] if model['name'].lower() == model_name.lower()), None)
            if model_config:
                preprocess_methods = select_preprocess_methods(config)
                print(f"\nRunning model: {model_config['name']}")
                print(f"Using preprocessing methods: {', '.join(preprocess_methods)}")
                run_model(model_config, data_file_path, preprocess_methods)
            else:
                print(f"Model '{model_name}' not found. Please try again.")

if __name__ == "__main__":
    main()
