import csv
import random
import os
from datetime import datetime, timedelta
from tqdm import tqdm

def generate_machine_data(num_rows):
    # 스크립트 파일의 디렉토리 경로 획득
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 현재 시간을 기반으로 파일명 생성
    current_time = datetime.now()
    file_name = f'data_{current_time.strftime("%m%d%Y_%H%M%S")}.csv'
    
    # 스크립트 디렉토리에 상대 경로로 파일 생성
    file_path = os.path.join(script_dir, file_name)
    
    fieldnames = [
        'Timestamp', 'Machine_ID', 'Material_Type', 'Cutting_Speed', 'Feed_Rate',
        'Depth_of_Cut', 'Tool_Usage_Time', 'Vibration', 'Coolant_Temperature',
        'Power_Consumption', 'Cycle_Time', 'Operator_ID', 'Batch_Number',
        'Product_ID', 'Tool_ID', 'Spindle_Speed', 'Spindle_Load', 'Feed_Load',
        'Axis_Position_X', 'Axis_Position_Y', 'Axis_Position_Z', 'Surface_Roughness',
        'Dimensional_Accuracy', 'Defect_Type', 'Quality_Result'
    ]

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        start_time = datetime.now()
        
        # tqdm을 사용하여 프로그레스 바 생성
        for _ in tqdm(range(num_rows), desc="Generating data", unit="rows"):
            row = {}
            for field in fieldnames:
                # 1% 확률로 빈 값 생성 (결측치 시뮬레이션)
                if random.random() < 0.01:
                    row[field] = ''
                else:
                    if field == 'Timestamp':
                        row[field] = (start_time + timedelta(minutes=random.randint(0, 1000000))).strftime("%Y-%m-%d %H:%M:%S")
                    elif field == 'Machine_ID':
                        row[field] = f'M{random.randint(1, 10):03d}'
                    elif field == 'Material_Type':
                        row[field] = random.choice(['Steel', 'Aluminum', 'Titanium', 'Copper'])
                    elif field == 'Cutting_Speed':
                        # 0.5% 확률로 음수 값 생성 (센서 오류 시뮬레이션)
                        row[field] = round(random.uniform(-10, 250) if random.random() < 0.005 else random.uniform(100, 250), 1)
                    elif field == 'Feed_Rate':
                        row[field] = round(random.uniform(0.1, 0.5), 2)
                    elif field == 'Depth_of_Cut':
                        row[field] = round(random.uniform(0.5, 3.0), 1)
                    elif field == 'Tool_Usage_Time':
                        row[field] = random.randint(60, 300)
                    elif field == 'Vibration':
                        row[field] = round(random.uniform(1.0, 5.0), 1)
                    elif field == 'Coolant_Temperature':
                        # 0.5% 확률로 비정상적으로 높은 온도 생성 (극단적 상황 시뮬레이션)
                        row[field] = round(random.uniform(20, 35) if random.random() > 0.005 else random.uniform(100, 150), 1)
                    elif field == 'Power_Consumption':
                        row[field] = round(random.uniform(3, 10), 1)
                    elif field == 'Cycle_Time':
                        row[field] = random.randint(200, 600)
                    elif field == 'Operator_ID':
                        row[field] = f'OP{random.randint(1, 20):03d}'
                    elif field == 'Batch_Number':
                        row[field] = f'B{random.randint(1, 100):03d}'
                    elif field == 'Product_ID':
                        row[field] = f'P{random.randint(1, 1000):04d}'
                    elif field == 'Tool_ID':
                        row[field] = f'T{random.randint(1, 50):03d}'
                    elif field == 'Spindle_Speed':
                        row[field] = random.randint(800, 2000)
                    elif field == 'Spindle_Load':
                        row[field] = round(random.uniform(50, 100), 1)
                    elif field == 'Feed_Load':
                        row[field] = round(random.uniform(40, 90), 1)
                    elif field in ['Axis_Position_X', 'Axis_Position_Y', 'Axis_Position_Z']:
                        # 0.5% 확률로 비정상적으로 큰 값 생성 (센서 오류 또는 극단적 상황 시뮬레이션)
                        row[field] = round(random.uniform(0, 500) if random.random() > 0.005 else random.uniform(1000, 2000), 1)
                    elif field == 'Surface_Roughness':
                        row[field] = round(random.uniform(1.0, 5.0), 1)
                    elif field == 'Dimensional_Accuracy':
                        row[field] = round(random.uniform(0.01, 0.1), 2)
                    elif field == 'Defect_Type':
                        row[field] = random.choice(['None', 'Scratch', 'Dent', 'Misalignment'])
                    elif field == 'Quality_Result':
                        # 90% 확률로 합격, 10% 확률로 불합격
                        row[field] = random.choices([0, 1], weights=[0.1, 0.9])[0]

            writer.writerow(row)

    print(f"\n{num_rows} rows of data have been generated in '{file_path}'")

# 10만 행의 데이터 생성
generate_machine_data(1000)