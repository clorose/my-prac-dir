import sys
from pathlib import Path
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import json
import argparse
from pathlib import Path
from datetime import datetime
from sklearn.metrics import classification_report
from models.xg_model import XGModel
from models.knn_model import KNNModel
from preprocessing.data_preprocessing import preprocess_data, print_data_ranges

def load_config():
    # __file__은 현재 파일(main.py)의 경로를 가져옵니다. 이를 바탕으로 config.json의 절대 경로를 얻습니다.
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    # config.json 파일을 열고, json.load()로 파싱하여 딕셔너리로 변환합니다.
    with open(config_path, 'r') as file:
        config = json.load(file)  # JSON 파싱
    return config


def load_model_class(model_name):
    if model_name.lower() == 'xg':
        return XGModel
    elif model_name.lower() == 'knn':
        return KNNModel
    else:
        raise ValueError(f"Unknown model: {model_name}")

def run_model(model_config, data_file_path, preprocess_method):
    model_class = load_model_class(model_config['name'])
    model = model_class()
    try:
        print(f"Model: {model_class.__name__}")
        print(f"Preprocess method: {preprocess_method}")
        model.load_data_and_train_model(data_file_path, preprocess_method, **model_config.get('params', {}))
        
        accuracy, f1, auc, report = model.get_model_performance()
        print(f"Accuracy: {accuracy * 100:.2f}%")
        print(f"F1 Score: {f1:.4f}")
        print(f"AUC: {auc:.4f}\n")
        
        print("Classification Report:")
        print(classification_report(model.y_test, model.model.predict(model.X_test), zero_division=1))
        
        if hasattr(model, 'get_feature_importance'):
            feature_importance = model.get_feature_importance()
            print("\nFeature Importances:")
            for feature, importance in feature_importance.items():
                print(f"{feature}: {importance:.2f}%")
        
        currentTime = datetime.now().strftime("%H%M%S")
        output_path = Path(__file__).parent / 'output' / f"processed_data_{model_class.__name__}_{currentTime}.csv"
        model.save_processed_data_to_csv(output_path)
        
        print_data_ranges(model.X_processed)
        
        model.plot_3d_scatter()
    
    except Exception as e:
        print(f"An error occurred in model execution: {e}")

def select_preprocess_method(config):
    print("\nAvailable preprocessing methods:")
    for method in config['preprocess_methods']:
        print(f"- {method}")
    
    while True:
        method = input("Enter the preprocessing method you want to use: ").lower()
        if method in config['preprocess_methods']:
            return method
        else:
            print(f"Invalid preprocessing method. Please choose from {', '.join(config['preprocess_methods'])}.")

def main():
    config = load_config()
    parser = argparse.ArgumentParser(description="Run machine learning models with preprocessing.")
    parser.add_argument('--model', type=str, choices=[model['name'] for model in config['models']], help="Select the model to run")
    parser.add_argument('--preprocess', type=str, choices=config['preprocess_methods'], help="Select the preprocessing method")
    args = parser.parse_args()

    data_file_path = Path(__file__).parent / 'data' / 'Machining_Factory_Data10000.csv'

    if args.model and args.preprocess:
        model_config = next(model for model in config['models'] if model['name'] == args.model)
        preprocess_method = args.preprocess
        print(f"Using model: {args.model}")
        print(f"Using preprocessing method: {preprocess_method}")
        run_model(model_config, data_file_path, preprocess_method)
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
                preprocess_method = select_preprocess_method(config)
                run_model(model_config, data_file_path, preprocess_method)
            else:
                print(f"Model '{model_name}' not found. Please try again.")

if __name__ == "__main__":
    main()