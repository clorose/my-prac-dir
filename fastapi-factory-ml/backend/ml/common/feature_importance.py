# Absolute path: C:\_YHJ\fast\backend\ml\common\feature_importance.py

def get_feature_importance(model, features):
    """
    Calculate feature importance for the given model.
    
    Args:
        model: Trained model with feature_importances_ attribute.
        features (list): List of feature names.

    Returns:
        dict: Feature importance scores sorted in descending order.
    """
    try:
        importance = model.feature_importances_
        importance = 100.0 * (importance / importance.max())
        return dict(sorted(zip(features, importance), key=lambda x: x[1], reverse=True))
    except Exception as e:
        print(f"An error occurred while calculating feature importance: {e}")
        raise
