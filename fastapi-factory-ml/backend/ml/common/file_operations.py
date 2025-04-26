# Absolute path: C:\_YHJ\fast\backend\ml\common\file_operations.py

import joblib
import pandas as pd

def save_model(model, file_path):
    """
    Save the trained model to a file.
    
    Args:
        model: Trained model to save.
        file_path (str): Path to save the model file.
    """
    try:
        joblib.dump(model, file_path)
        print(f"Model saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the model: {e}")
        raise

def load_model(file_path):
    """
    Load a trained model from a file.
    
    Args:
        file_path (str): Path to the model file.

    Returns:
        Loaded model.
    """
    try:
        model = joblib.load(file_path)
        print(f"Model loaded from {file_path}")
        return model
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        raise

def save_data_to_csv(data, file_path):
    """
    Save processed data to a CSV file.
    
    Args:
        data (pd.DataFrame): Data to save.
        file_path (str): Path to save the CSV file.
    """
    try:
        data.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving data to CSV: {e}")
        raise
