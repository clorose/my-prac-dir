import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
import joblib
import os

OUTPUT_DIR = "C:/_YHJ/fast/backend/ml/output"

def run_model(file_path, target_column=None):
    try:
        # 데이터 로드
        data = pd.read_csv(file_path)
        
        # 타겟 열 처리
        if target_column is None:
            # 기본값으로 'quality_label' 사용
            target_column = 'quality_label'
        
        if target_column not in data.columns:
            return {"error": f"Specified target column '{target_column}' not found in the dataset."}
        
        # 특성과 타겟 분리
        X = data.drop(target_column, axis=1)
        y = data[target_column]
        
        # 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 모델 학습
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # 예측 및 성능 평가
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions, average='weighted')
        try:
            auc = roc_auc_score(y_test, model.predict_proba(X_test), multi_class='ovr', average='weighted')
        except ValueError:
            auc = None  # AUC를 계산할 수 없는 경우 (예: 이진 분류가 아닌 경우)
        
        # 분류 보고서 생성
        report = classification_report(y_test, predictions, output_dict=True)
        
        # 모델 저장
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        model_path = os.path.join(OUTPUT_DIR, "model.joblib")
        joblib.dump(model, model_path)
        
        return {
            "accuracy": accuracy,
            "f1_score": f1,
            "auc": auc,
            "classification_report": report,
            "model_path": model_path,
            "feature_importance": dict(zip(X.columns, model.feature_importances_))
        }
    
    except Exception as e:
        return {"error": str(e)}