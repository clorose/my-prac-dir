# 프로젝트 루트 찾아가기 - 현재 생각하는 제일 유연한 방법

프로젝트 내 어디서든 루트 디렉토리를 찾고 참조할 수 있는 유틸리티입니다.

### 장점
- **호출 위치 기반**: 실제 호출한 파일의 위치에서부터 검색을 시작하므로 어디서든 사용 가능
- **구조 독립적**: 프로젝트 구조가 변경되어도 영향 없음
- **마커 파일 커스터마이즈**: `.project_root` 외에 다른 마커 파일도 지정 가능

### 사용 예시
```python
from utils.pathfinder import find_project_root, get_project_path

# 프로젝트 루트 찾기
root = find_project_root()
print(f"프로젝트 루트: {root}")

# 특정 파일/디렉토리 경로 가져오기
config_path = get_project_path('config/settings.yaml')
data_path = get_project_path('data/processed')
```

더 나은 방법을 발견하면 계속 업데이트할 예정이며, 충분히 검증되면 pip 패키지로도 배포할 계획입니다.
이런 라이브러리가 실제로 있다해도 그냥 pip 배포 해보고 싶어서 아마 배포 하지 않을까 싶습니다.