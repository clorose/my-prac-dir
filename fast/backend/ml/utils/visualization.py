# ml\utils\visualization.py

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties

# 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'
fontprop = FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

def select_top_features(X_processed, feature_importances, top_n=3):
    # 특성 중요도에 따라 상위 N개의 특성 선택
    top_indices = np.argsort(feature_importances)[-top_n:]
    top_features = [X_processed.columns[i] for i in top_indices]
    return X_processed[top_features], top_features

def stratified_sampling(X_processed, y_processed, sample_size_per_class=500):
    df = pd.concat([X_processed, y_processed], axis=1)
    df.columns = list(X_processed.columns) + ['target']
    sampled_df = df.groupby('target', group_keys=False).apply(lambda x: x.sample(n=min(len(x), sample_size_per_class)))
    sampled_df = sampled_df.reset_index(drop=True)
    X_sample = sampled_df.drop('target', axis=1)
    y_sample = sampled_df['target']
    return X_sample, y_sample

def plot_3d_scatter(X_sampled, y_sampled, top_features):
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    scatter = ax.scatter(X_sampled.iloc[:, 0], 
                         X_sampled.iloc[:, 1], 
                         X_sampled.iloc[:, 2], 
                         c=y_sampled, 
                         cmap='viridis', 
                         alpha=0.6)
    
    ax.set_xlabel(top_features[0])
    ax.set_ylabel(top_features[1])
    ax.set_zlabel(top_features[2])
    ax.set_title('상위 3개 중요한 특성에 대한 3D 산점도', fontproperties=fontprop)
    
    plt.colorbar(scatter)
    plt.tight_layout()
    plt.show()

def plot_scatter_matrix(X_sampled, y_sampled):
    df = X_sampled.copy()
    df['target'] = y_sampled
    
    sns.set(style="ticks", color_codes=True)
    g = sns.pairplot(df, hue='target', vars=X_sampled.columns, plot_kws={'s': 20, 'alpha': 0.5})
    g.fig.suptitle('Scatter Plot Matrix (Sampled Data)', y=1.02)
    plt.show()

def plot_correlation_heatmap(X_sampled):
    plt.figure(figsize=(12, 10))
    corr = X_sampled.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap (Top Features)')
    plt.show()

def plot_feature_importance(features, feature_importances, top_n=10):
    # 상위 n개의 특성 선택
    indices = np.argsort(feature_importances)[-top_n:]
    pos = np.arange(len(indices)) + .5
    fig = plt.figure(figsize=(12, 6))
    plt.barh(pos, np.array(feature_importances)[indices], align='center')
    plt.yticks(pos, np.array(features)[indices])
    plt.title(f'Top {top_n} Feature Importances')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()

def plot_box_plots(X_sampled, y_sampled, top_features):
    fig, axes = plt.subplots(1, len(top_features), figsize=(5 * len(top_features), 6))
    if len(top_features) == 1:
        axes = [axes]
    for idx, column in enumerate(top_features):
        sns.boxplot(x=y_sampled, y=X_sampled[column], ax=axes[idx])
        axes[idx].set_title(f'Box Plot of {column}')
    plt.tight_layout()
    plt.show()

def visualize_data(X_processed, y_processed, features, feature_importances, time_data=None):
    # 상위 N개의 중요한 특성 선택 (여기서는 상위 3개)
    X_top_features, top_features = select_top_features(X_processed, feature_importances, top_n=3)
    
    # 데이터 샘플링 (층화 샘플링)
    X_sampled, y_sampled = stratified_sampling(X_top_features, y_processed, sample_size_per_class=500)
    
    while True:
        print("\nAvailable visualizations:")
        print("1. 3D Scatter Plot (Top Features)")
        print("2. Scatter Plot Matrix (Top Features)")
        print("3. Correlation Heatmap (Top Features)")
        print("4. Feature Importance")
        print("5. Box Plots (Top Features)")
        print("6. Exit")
        
        choice = input("원하는 시각화 번호를 입력하세요 (또는 6을 눌러 종료): ")
        
        if choice == '1':
            plot_3d_scatter(X_sampled, y_sampled, top_features)
        elif choice == '2':
            plot_scatter_matrix(X_sampled, y_sampled)
        elif choice == '3':
            plot_correlation_heatmap(X_sampled)
        elif choice == '4':
            plot_feature_importance(features, feature_importances)
        elif choice == '5':
            plot_box_plots(X_sampled, y_sampled, top_features)
        elif choice == '6':
            break
        else:
            print("잘못된 입력입니다. 다시 시도해주세요.")

# 예시 사용법:
# 모델 훈련 후에 feature_importances를 얻어야 합니다.
# 예를 들어, feature_importances = model.get_feature_importance()
# 그 다음 visualize_data 함수를 호출합니다.
# visualize_data(X_processed, y_processed, features, feature_importances)
