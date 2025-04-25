# visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from pathlib import Path
import numpy as np
from datetime import datetime

class MNISTVisualizer:
    """MNIST 학습 과정 시각화를 위한 클래스"""

    def __init__(self, save_dir='visualizations'):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.history = []

    def plot_sample_images(self, images, labels, predictions=None, num_samples=10):
        """샘플 이미지 시각화"""
        plt.figure(figsize=(15, 3))
        for i in range(min(num_samples, len(images))):
            plt.subplot(1, num_samples, i + 1)
            plt.imshow(images[i].reshape(28, 28), cmap='gray')
            title = f'Label: {labels[i]}'
            if predictions is not None:
                title += f'\nPred: {predictions[i]}'
            plt.title(title)
            plt.axis('off')
        return self._save_figure('sample_images.png')

    def plot_training_history(self, history):
        """학습 히스토리 시각화"""
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='training')
        plt.plot(history.history['val_accuracy'], label='validation')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='training')
        plt.plot(history.history['val_loss'], label='validation')
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()

        return self._save_figure('training_history.png')

    def plot_confusion_matrix(self, y_true, y_pred):
        """혼동 행렬 시각화"""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        return self._save_figure('confusion_matrix.png')

    def _save_figure(self, filename):
        """현재 figure를 파일로 저장하고 경로 반환"""
        filepath = self.save_dir / filename
        plt.savefig(filepath)
        plt.close()
        return filepath

    def generate_report(self, model_info, training_history):
        """학습 결과 리포트 생성"""
        report_path = self.save_dir / 'training_report.html'
        with open(report_path, 'w') as f:
            f.write(self._generate_html_report(model_info, training_history))
        return report_path

    def _generate_html_report(self, model_info, training_history):
        """HTML 리포트 내용 생성"""
        html = f"""
        <html>
        <head>
            <title>MNIST Training Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .metric {{ padding: 20px; background: #f5f5f5; border-radius: 5px; text-align: center; }}
                .metric h3 {{ color: #333; margin-top: 0; }}
                .metric p {{ font-size: 24px; margin: 10px 0; color: #2196F3; }}
                img {{ max-width: 100%; height: auto; margin: 10px 0; }}
                pre {{ white-space: pre-wrap; background: #f5f5f5; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>MNIST 학습 결과 리포트</h1>
            <div class="section">
                <h2>학습 요약</h2>
                <div class="grid">
                    <div class="metric">
                        <h3>최종 정확도</h3>
                        <p>{training_history.history['val_accuracy'][-1]:.4f}</p>
                    </div>
                    <div class="metric">
                        <h3>최종 손실값</h3>
                        <p>{training_history.history['val_loss'][-1]:.4f}</p>
                    </div>
                    <div class="metric">
                        <h3>총 에포크</h3>
                        <p>{len(training_history.history['accuracy'])}</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>학습 과정 시각화</h2>
                <img src="training_history.png" alt="Training History" />
                <p>파란색: 학습 데이터, 주황색: 검증 데이터</p>
            </div>

            <div class="section">
                <h2>샘플 이미지 예측</h2>
                <img src="sample_images.png" alt="Sample Predictions" />
            </div>

            <div class="section">
                <h2>혼동 행렬</h2>
                <img src="confusion_matrix.png" alt="Confusion Matrix" />
                <p>행: 실제 클래스, 열: 예측 클래스</p>
            </div>

            <div class="section">
                <h2>모델 구조</h2>
                <pre>{model_info}</pre>
            </div>

            <div class="section">
                <h2>생성 시간</h2>
                <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        return html