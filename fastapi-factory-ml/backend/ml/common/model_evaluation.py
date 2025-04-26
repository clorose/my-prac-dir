# Absolute path: C:\_YHJ\fast\backend\ml\common\model_evaluation.py

from sklearn.metrics import accuracy_score, classification_report, f1_score, roc_auc_score

def evaluate_model_performance(model, X_test, y_test):
    """
    Evaluate model performance using various metrics.
    
    Args:
        model: Trained model.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): True labels for the test set.

    Returns:
        tuple: accuracy, f1, auc, classification report as a dictionary
    """
    try:
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)
        
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=1)
        
        return accuracy, f1, auc, report
    except Exception as e:
        print(f"An error occurred while evaluating the model: {e}")
        raise
