import torch
import torchvision
from ultralytics import YOLO
import cv2
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorboard import summary
import yaml
from tqdm import tqdm
import os
from dotenv import load_dotenv

def test_libraries():
    # 기본 파이썬 테스트
    print("Basic Python Test: Hello from Docker!")
    
    # CUDA 가용성 테스트
    print("\nPyTorch CUDA Test:")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    
    # OpenCV 테스트
    print(f"\nOpenCV version: {cv2.__version__}")
    
    # Numpy 테스트
    arr = np.array([1, 2, 3])
    print(f"\nNumPy Test: {arr}")
    
    # Pandas 테스트
    df = pd.DataFrame({'test': [1, 2, 3]})
    print(f"\nPandas Test:\n{df}")
    
    # 환경변수 테스트
    load_dotenv()
    print("\nEnvironment variables loaded")
    
    # YOLO 버전 테스트
    print(f"\nUltralytics version: {YOLO._version}")
    
    print("\nAll libraries imported successfully!")

if __name__ == "__main__":
    test_libraries()