import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

def plot_3d_scatter(X_processed, y_processed, features, feature_importances=None):
    if feature_importances is not None:
        top_features = sorted(zip(features, feature_importances), key=lambda x: x[1], reverse=True)[:3]
        top_feature_names = [f[0] for f in top_features]
    else:
        top_feature_names = features[:3]

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(X_processed[top_feature_names[0]], 
                         X_processed[top_feature_names[1]], 
                         X_processed[top_feature_names[2]], 
                         c=y_processed, 
                         cmap='viridis', 
                         alpha=0.6)

    ax.set_xlabel(top_feature_names[0])
    ax.set_ylabel(top_feature_names[1])
    ax.set_zlabel(top_feature_names[2])
    ax.set_title('3D Scatter Plot of Top 3 Features\nColor indicates Target Variable')

    plt.colorbar(scatter)
    plt.tight_layout()
    plt.show()

def plot_scatter_matrix(X_processed, y_processed):
    df = X_processed.copy()
    df['target'] = y_processed
    sns.pairplot(df, hue='target', vars=X_processed.columns)
    plt.suptitle('Scatter Plot Matrix', y=1.02)
    plt.show()

def plot_correlation_heatmap(X_processed):
    plt.figure(figsize=(12, 10))
    sns.heatmap(X_processed.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()

def plot_feature_importance(features, feature_importances):
    sorted_idx = feature_importances.argsort()
    pos = np.arange(sorted_idx.shape[0]) + .5
    fig = plt.figure(figsize=(12, 6))
    plt.barh(pos, feature_importances[sorted_idx], align='center')
    plt.yticks(pos, np.array(features)[sorted_idx])
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()

def plot_box_plots(X_processed, y_processed):
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    axes = axes.ravel()
    for idx, column in enumerate(X_processed.columns[:6]):  # 처음 6개 특성에 대해서만 박스 플롯 생성
        sns.boxplot(x=y_processed, y=X_processed[column], ax=axes[idx])
        axes[idx].set_title(f'Box Plot of {column}')
    plt.tight_layout()
    plt.show()

def visualize_data(X_processed, y_processed, features, feature_importances=None):
    while True:
        print("\nAvailable visualizations:")
        print("1. 3D Scatter Plot")
        print("2. Scatter Plot Matrix")
        print("3. Correlation Heatmap")
        print("4. Feature Importance")
        print("5. Box Plots")
        print("6. Exit")
        
        choice = input("Enter the number of the visualization you want to see (or 6 to exit): ")
        
        if choice == '1':
            plot_3d_scatter(X_processed, y_processed, features, feature_importances)
        elif choice == '2':
            plot_scatter_matrix(X_processed, y_processed)
        elif choice == '3':
            plot_correlation_heatmap(X_processed)
        elif choice == '4':
            if feature_importances is not None:
                plot_feature_importance(features, feature_importances)
            else:
                print("Feature importance information is not available.")
        elif choice == '5':
            plot_box_plots(X_processed, y_processed)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

# 메인 스크립트에서 이 함수를 호출하여 사용
# visualize_data(X_processed, y_processed, features, feature_importances)