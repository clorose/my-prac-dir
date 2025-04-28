from utils.pathfinder import find_project_root, get_project_path

# 프로젝트 루트 찾기
root = find_project_root()
print(f"프로젝트 루트: {root}")

# 특정 경로 찾기 (예: config 파일)
config_path = get_project_path('config/settings.yaml')
print(f"설정 파일 경로: {config_path}")