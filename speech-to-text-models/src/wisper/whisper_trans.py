import whisper
import os
from datetime import datetime
from pathlib import Path
from src.utils.pathfinder import get_project_path, setup_project_path

setup_project_path()

def get_model(model_name: str = "turbo") -> whisper.Whisper:
    """모델을 models 디렉토리에서 로드하거나 다운로드"""
    model_dir = get_project_path('models')
    if model_dir is None:
        raise RuntimeError("Project root not found")
    
    # 환경변수 설정하여 모델 저장 위치 변경
    os.environ["XDG_CACHE_HOME"] = str(model_dir)
    print(f"Loading model from/to: {model_dir}")
    
    return whisper.load_model(model_name)

def save_transcription(text: str) -> Path:
    """변환된 텍스트를 runs 디렉토리에 저장"""
    runs_dir = get_project_path('runs')
    if runs_dir is None:
        raise RuntimeError("Project root not found")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = runs_dir / f"transcription_{timestamp}.txt"
    
    output_file.write_text(text, encoding="utf-8")
    print(f"Transcription saved to: {output_file}")
    
    return output_file

def main():
    # 모델 로드
    model = get_model()
    
    # 오디오 파일 경로
    audio_path = get_project_path('src/wisper/example3.mp4')
    if audio_path is None:
        raise RuntimeError("Audio file not found")
    
    # 변환 실행
    print(f"Transcribing: {audio_path}")
    result = model.transcribe(str(audio_path))
    
    # 결과 저장
    text = result["text"]
    save_transcription(text)
    
    # 콘솔에도 출력
    print("\nTranscription:")
    print(text)

if __name__ == "__main__":
    main()