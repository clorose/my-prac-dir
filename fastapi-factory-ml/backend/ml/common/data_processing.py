# Absolute path: C:\_YHJ\fast\backend\ml\common\data_processing.py

from sklearn.model_selection import train_test_split

def split_data(X, y, id_material, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets.
    
    Args:
        X (pd.DataFrame): Feature data.
        y (pd.Series): Target data.
        id_material (pd.Series): Identifier for each sample.
        test_size (float): Proportion of the data to use for the test set.
        random_state (int): Seed for reproducibility.

    Returns:
        tuple: X_train, X_test, y_train, y_test, id_material_train, id_material_test
    """
    return train_test_split(X, y, id_material, test_size=test_size, random_state=random_state)
