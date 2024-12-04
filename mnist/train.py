# train.py
import tensorflow as tf
import numpy as np
from pathlib import Path
from visualizer import MNISTVisualizer
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

def prepare_data():
    """데이터 준비 및 전처리"""
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0

    X_train = X_train.reshape(-1, 28, 28, 1)
    X_test = X_test.reshape(-1, 28, 28, 1)

    return X_train, y_train, X_test, y_test

def create_model():
    """M3 Pro 에 최적화된 모델 생성"""
    # MPS 가속기 설정
    if tf.config.list_physical_devices('GPU'):
        try:
            tf.config.experimental.set_visible_devices(
                tf.config.list_physical_devices('GPU')[0], 'GPU'
            )
            logging.info("MPS 가속기가 활성화되었습니다.")
        except Exception as e:
            logging.warning(f"MPS 가속기 설정 실패: {e}")

    model = tf.keras.Sequential([
        # 1번째 Convolution Block
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # 2번째 Convolution Block
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # Fully Connected Layers
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

def main():
    try:
        # 시각화 도구 초기화
        visualizer = MNISTVisualizer()

        # 데이터 준비
        X_train, y_train, X_test, y_test = prepare_data()

        # 모델 생성
        model = create_model()
        model.summary()

        # 모델 학습
        history = model.fit(
            X_train, y_train,
            epochs=20,  # 20 에포크로 설정
            validation_split=0.2,
            batch_size=32,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    patience=5,  # 5 에포크동안 개선이 없으면 조기 종료
                    restore_best_weights=True
                )
            ]
        )

        # 테스트 평가
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=2)
        logging.info(f"\n테스트 정확도: {test_accuracy * 100:.2f}%")

        # 예측
        predictions = model.predict(X_test)

        # 시각화 및 리포트 생성
        visualizer.plot_sample_images(X_test[:10], y_test[:10], predictions.argmax(axis=1)[:10])
        visualizer.plot_training_history(history)
        visualizer.plot_confusion_matrix(y_test, predictions.argmax(axis=1))

        # 모델 정보 문자열 생성
        stringlist = []
        model.summary(print_fn=lambda x: stringlist.append(x))
        model_info = "\n".join(stringlist)

        # 리포트 생성
        report_path = visualizer.generate_report(model_info, history)
        logging.info(f"\n학습 리포트가 생성되었습니다: {report_path}")

        # 모델 저장
        model.save('mnist_model.keras')
        logging.info("\n모델이 'mnist_model.keras'로 저장되었습니다.")

    except Exception as e:
        logging.error(f"학습 중 오류 발생: {e}")
        raise

if __name__ == "__main__":
    main()