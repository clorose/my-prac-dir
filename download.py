import tensorflow as tf  # keras가 여기 포함되어 있음
import numpy as np
import matplotlib.pyplot as plt

# MNIST 데이터 다운로드
print("MNIST 데이터 다운로드 시작...")
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
print("다운로드 완료!")

# 데이터 정보 출력
print(f"\n학습 데이터:")
print(f"이미지 데이터 크기: {X_train.shape}")  # (60000, 28, 28)
print(f"레이블 데이터 크기: {y_train.shape}")  # (60000,)
print(f"\n테스트 데이터:")
print(f"이미지 데이터 크기: {X_test.shape}")   # (10000, 28, 28)
print(f"레이블 데이터 크기: {y_test.shape}")   # (10000,)

# 예시 이미지 확인
plt.figure(figsize=(10, 5))
for i in range(5):
    plt.subplot(1, 5, i+1)
    plt.imshow(X_train[i], cmap='gray')
    plt.title(f'Label: {y_train[i]}')
    plt.axis('off')
plt.show()