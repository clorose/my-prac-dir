# fpath: src/wisper/test.py
from src.utils.pathfinder import find_project_root, get_project_path, setup_project_path

setup_project_path()

def main():
    root = find_project_root()
    print(f"프로젝트 루트: {root}")
    
    # 테스트로 몇 가지 경로 출력
    utils_path = get_project_path('src/utils')
    print(f"utils 경로: {utils_path}")

if __name__ == "__main__":
    main()