# MNIST 숫자 인식 프로젝트 연구노트

## 1. 프로젝트 개요
- **목적**: MNIST 데이터셋을 활용한 손글씨 숫자 인식 시스템 개발
- **개발 환경**: 
    - Python 3.9 이상
    - TensorFlow 2.18.0 이상: 머신 러닝 프레임워크
    - scikit-learn 1.5.2 이상: 머신 러닝 라이브러리
    - Matplotlib 3.9.2 이상: 시각화 라이브러리
    - Seaborn 0.13.2 이상: 시각화 라이브러리
    - NumPy 2.0.2 이상: 수치 연산 라이브러리
    - Pillow 11.0.0 이상: 이미지 처리 라이브러리
    - PyQt6 6.7.1 이상: GUI 프레임워크
    - MNIST 데이터셋: 손글씨 숫자 데이터셋(60,000개 학습 데이터, 10,000개 테스트 데이터)

## 2. 프로젝트 구조
프로젝트는 다음과 같이 주요 모듈로 구성되어 있습니다:

```
.
├── download.py          # MNIST 데이터셋 다운로드 및 기본 시각화
├── main.py              # 기본 PyCharm 생성 파일
├── predict.py           # 숫자 인식을 위한 GUI 애플리케이션
├── requirements.txt     # 필요한 패키지 목록
├── train.py             # 모델 학습 스크립트
├── visualizer.py        # 학습 과정 및 결과 시각화 도구
└── training_report.html # 학습 결과 리포트
```

## 3. 구현 세부사항

### 3.1 데이터 전처리
- 이미지 정규화 (0-255 → 0-1)
  ```python
  X_train = X_train.astype('float32') / 255.0
  X_test = X_test.astype('float32') / 255.0
  ```
- 28x28 크기의 흑백 이미지를 CNN 입력에 맞게 형태 변환
  ```python
  X_train = X_train.reshape(-1, 28, 28, 1)
  X_test = X_test.reshape(-1, 28, 28, 1)
  ```
- 훈련 데이터 60,000개, 테스트 데이터 10,000개로 구성
  ```python
  (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
  ```

### 3.2 모델 아키텍처
CNN 구조:
```python
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
```

- 2개의 Convolution Block으로 구성:
  - 첫 번째 블록: 32개의 3x3 필터와 ReLU 활성화 함수, 2x2 맥스 풀링
  - 두 번째 블록: 64개의 3x3 필터와 ReLU 활성화 함수, 2x2 맥스 풀링
- 완전 연결 레이어:
  - Flatten 레이어: 2D 특성 맵을 1D 벡터로 변환
  - 64개 노드를 가진 은닉층 (ReLU 활성화)
  - 10개 노드를 가진 출력층 (소프트맥스 활성화)
- 총 파라미터: 121,930개 (476.29 KB)
  - 훈련 가능 파라미터: 121,930개
  - 최적화 파라미터: 243,862개 (952.59 KB)

소프트맥스 함수는 다중 클래스 분류 문제에서 사용되는 활성화 함수로, 각 클래스(0-9 숫자)에 대한 확률 분포를 출력합니다.

### 3.3 학습 파라미터 및 전략
```python
# 모델 컴파일
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

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
```

- **최적화 알고리즘**: Adam (적응형 학습률 최적화 알고리즘)
- **손실 함수**: Sparse Categorical Crossentropy (다중 클래스 분류에 적합)
- **평가 지표**: Accuracy (정확도)
- **학습 하이퍼파라미터**:
  - 최대 에포크 수: 20
  - 배치 크기: 32
  - 검증 데이터 비율: 20%
- **조기 종료 전략**: 
  - 검증 손실이 5 에포크 동안 개선되지 않으면 학습 중단
  - 최적의 가중치 자동 복원

실제 학습에서는 조기 종료로 인해 10 에포크에서 학습이 완료되었습니다.

### 3.4 성능 평가
학습 결과 모델이 달성한 성능 지표:
- **최종 검증 정확도**: 98.87%
- **최종 검증 손실값**: 0.0492

테스트 셋에 대한 최종 평가는 train.py에서 다음과 같이 수행됩니다:
```python
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=2)
logging.info(f"\n테스트 정확도: {test_accuracy * 100:.2f}%")
```

### 3.5 GUI 구현
PyQt6를 사용하여 직관적인 사용자 인터페이스를 구현했습니다:

```python
class MNISTPredictorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.initUI()
        self.load_model()
```

주요 GUI 기능:
- **드래그 앤 드롭 이미지 입력**: 사용자가 이미지를 GUI에 직접 끌어다 놓을 수 있음
- **파일 브라우저**: 이미지 파일을 탐색기에서 선택 가능
- **실시간 예측**: 업로드된 이미지에 대한 즉시 예측 제공
- **확률 분포 시각화**: 각 숫자(0-9)에 대한 예측 확률을 바 차트로 표시
- **피드백 UI**: 예측 결과와 확률을 명확하게 표시하는 레이블

이미지 전처리를 위해 PIL 라이브러리를 활용하여 업로드된 이미지를 28x28 크기의 흑백 이미지로 변환합니다.

## 4. 시각화 및 분석
프로젝트는 MNISTVisualizer 클래스를 통해 다양한 시각화 기능을 제공합니다:

```python
class MNISTVisualizer:
    """MNIST 학습 과정 시각화를 위한 클래스"""

    def __init__(self, save_dir='visualizations'):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.history = []
```

주요 시각화 기능:
- **학습 곡선**: 에포크별 정확도와 손실 그래프
  ```python
  def plot_training_history(self, history):
      """학습 히스토리 시각화"""
      # 코드 구현...
  ```
- **혼동 행렬**: 실제 레이블과 예측 레이블 간의 관계를 보여주는 히트맵
  ```python
  def plot_confusion_matrix(self, y_true, y_pred):
      """혼동 행렬 시각화"""
      # 코드 구현...
  ```
- **샘플 예측 결과**: 테스트 이미지에 대한 예측 시각화
  ```python
  def plot_sample_images(self, images, labels, predictions=None, num_samples=10):
      """샘플 이미지 시각화"""
      # 코드 구현...
  ```
- **HTML 형식의 종합 리포트**: 학습 결과와 모델 구조를 포함한 상세한 보고서
  ```python
  def generate_report(self, model_info, training_history):
      """학습 결과 리포트 생성"""
      # 코드 구현...
  ```

## 5. 특이사항 및 최적화
- **Apple Silicon 최적화**: M3 Pro 프로세서에 최적화된 모델 구조
  ```python
  # MPS 가속기 설정
  if tf.config.list_physical_devices('GPU'):
      try:
          tf.config.experimental.set_visible_devices(
              tf.config.list_physical_devices('GPU')[0], 'GPU'
          )
          logging.info("MPS 가속기가 활성화되었습니다.")
      except Exception as e:
          logging.warning(f"MPS 가속기 설정 실패: {e}")
  ```
- **과적합 방지 전략**: 조기 종료(Early Stopping)를 통한 과적합 방지
- **자동 리포트 생성**: 학습 결과와 모델 성능을 자동으로 HTML 리포트로 생성
- **로깅 시스템**: 학습 및 예측 과정에서 발생하는 정보와 오류를 체계적으로 기록

## 6. 향후 개선 방향
- **데이터 증강(Data Augmentation)**: 회전, 이동, 확대/축소 등의 변환을 통한 학습 데이터 다양화
- **모델 구조 개선**: ResNet, DenseNet 등의 더 복잡한 CNN 아키텍처 적용
- **하이퍼파라미터 최적화**: 그리드 서치나 베이지안 최적화를 통한 최적 파라미터 탐색
- **앙상블 기법**: 여러 모델의 예측을 결합하여 정확도 향상
- **실시간 학습**: 사용자 피드백을 통한 모델 지속 개선 시스템 구현

## 7. 결론
이 프로젝트는 MNIST 데이터셋을 활용하여 98.87%의 높은 정확도를 달성한 손글씨 숫자 인식 시스템을 성공적으로 구현했습니다. CNN 모델과 PyQt6 기반 GUI를 통합하여 사용자 친화적인 애플리케이션을 개발했으며, 자동화된 시각화 및 리포팅 시스템을 통해 모델 성능을 직관적으로 분석할 수 있습니다. Apple Silicon에 최적화된 구현으로 효율적인 학습과 추론이 가능하며, 손글씨 인식 분야의 다른 문제에도 확장 적용할 수 있는 기반을 마련했습니다.