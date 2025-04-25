# predict_gui.py
import sys
import numpy as np
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DropLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("이미지를 드래그 앤 드롭하세요\n또는 클릭하여 선택")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 20px;
                background: #f0f0f0;
            }
        """)
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 200)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasImage or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasImage:
            self.parent().handle_image(event.mimeData().imageData())
        elif event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toLocalFile()
            self.parent().load_image_file(url)


class MNISTPredictorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.initUI()
        self.load_model()

    def initUI(self):
        self.setWindowTitle('MNIST 숫자 예측기')
        self.setMinimumSize(800, 400)

        # 메인 위젯과 레이아웃
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # 왼쪽 패널 (이미지 업로드)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.image_label = DropLabel(self)
        self.image_label.mousePressEvent = self.open_file_dialog

        left_layout.addWidget(self.image_label)
        layout.addWidget(left_panel)

        # 오른쪽 패널 (예측 결과)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # 예측 결과 레이블
        self.result_label = QLabel("예측 결과가 여기에 표시됩니다")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.result_label)

        # Matplotlib Figure 추가
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        right_layout.addWidget(self.canvas)

        layout.addWidget(right_panel)

        # 스타일 설정
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                padding: 5px 10px;
                font-size: 14px;
            }
        """)

    def load_model(self):
        try:
            self.model = tf.keras.models.load_model('mnist_model.keras')
        except:
            try:
                self.model = tf.keras.models.load_model('mnist_model.h5')
            except Exception as e:
                self.result_label.setText(f"모델 로드 실패: {str(e)}")

    def open_file_dialog(self, event):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "이미지 선택",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.load_image_file(file_name)

    def load_image_file(self, file_path):
        try:
            # PIL로 이미지 로드
            image = Image.open(file_path).convert('L')  # 흑백으로 변환
            image = image.resize((28, 28))  # MNIST 크기로 리사이즈

            # QLabel에 표시하기 위한 변환
            img_array = np.array(image)
            height, width = img_array.shape
            bytes_per_line = width
            q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

            # 예측을 위한 전처리
            img_array = np.array(image).astype('float32') / 255.0
            img_array = np.expand_dims(img_array, axis=(0, -1))

            # 예측 수행
            self.predict(img_array)

        except Exception as e:
            self.result_label.setText(f"이미지 로드 실패: {str(e)}")

    def handle_image(self, image_data):
        try:
            # QImage를 PIL Image로 변환
            image = Image.fromqimage(image_data).convert('L')
            image = image.resize((28, 28))

            # QLabel에 표시
            pixmap = QPixmap.fromImage(image_data)
            scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

            # 예측을 위한 전처리
            img_array = np.array(image).astype('float32') / 255.0
            img_array = np.expand_dims(img_array, axis=(0, -1))

            # 예측 수행
            self.predict(img_array)

        except Exception as e:
            self.result_label.setText(f"이미지 처리 실패: {str(e)}")

    def predict(self, image):
        if self.model is None:
            self.result_label.setText("모델이 로드되지 않았습니다!")
            return

        # 예측 수행
        predictions = self.model.predict(image)
        predicted_digit = np.argmax(predictions[0])
        confidence = predictions[0][predicted_digit] * 100

        # 결과 텍스트 업데이트
        self.result_label.setText(f"예측된 숫자: {predicted_digit}\n확률: {confidence:.2f}%")

        # 그래프 업데이트
        self.ax.clear()
        self.ax.bar(range(10), predictions[0])
        self.ax.set_title('예측 확률 분포')
        self.ax.set_xlabel('숫자')
        self.ax.set_ylabel('확률')
        self.ax.set_xticks(range(10))
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = MNISTPredictorGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()