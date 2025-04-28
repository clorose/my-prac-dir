# fpath: src/utils/pathfinder.py
from pathlib import Path
import inspect
import sys
from typing import Optional, Union

class ProjectRootNotFoundError(Exception):
    """프로젝트 루트를 찾을 수 없을 때 발생하는 예외"""
    pass

def find_project_root(marker: str = '.project_root', max_depth: int = 10) -> Optional[Path]:
    """프로젝트 루트 디렉토리를 찾아 반환합니다.
    
    Args:
        marker: 루트 디렉토리를 식별하는 마커 파일명
        max_depth: 최대 탐색 깊이 (무한루프 방지)
        
    Returns:
        Path: 프로젝트 루트 디렉토리 경로
        None: 프로젝트 루트를 찾지 못한 경우
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return None
            
        # 호출자의 파일 경로 얻기
        caller_file = Path(frame.f_back.f_code.co_filename).resolve()
        current = caller_file.parent
        
        for _ in range(max_depth):
            if (current / marker).exists():
                return current
            
            if current == current.parent:  # 루트 디렉토리에 도달
                break
                
            current = current.parent
            
        return None
        
    finally:
        # 참조 정리
        del frame

def setup_project_path() -> bool:
    """프로젝트 루트를 Python path에 추가하여 어디서든 import 가능하게 합니다.
    
    Returns:
        bool: 설정 성공 여부
    """
    root = find_project_root()
    if root is not None:
        root_str = str(root)
        if root_str not in sys.path:
            sys.path.append(root_str)
            return True
    return False

def get_project_path(relative_path: Union[str, Path], strict: bool = False) -> Optional[Path]:
    """프로젝트 루트 기준의 상대 경로를 절대 경로로 변환합니다.
    
    Args:
        relative_path: 프로젝트 루트 기준 상대 경로
        strict: True인 경우 루트를 찾지 못하면 예외 발생
        
    Returns:
        Path: 절대 경로
        None: strict=False이고 프로젝트 루트를 찾지 못한 경우
        
    Raises:
        ProjectRootNotFoundError: strict=True이고 프로젝트 루트를 찾지 못한 경우
        
    Example:
        >>> get_project_path('config/settings.yaml')
        PosixPath('/project/root/config/settings.yaml')
    """
    root = find_project_root()
    
    if root is None:
        if strict:
            raise ProjectRootNotFoundError(
                "프로젝트 루트를 찾을 수 없습니다. "
                "프로젝트 루트 디렉토리에 .project_root 파일이 있는지 확인하세요."
            )
        return None
        
    return root / Path(relative_path)