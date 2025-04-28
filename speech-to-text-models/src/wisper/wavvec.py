import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from datetime import datetime
from pathlib import Path
import soundfile as sf
import subprocess
from src.utils.pathfinder import get_project_path, setup_project_path

setup_project_path()

def get_model(language: str = "ko") -> tuple[Wav2Vec2Processor, Wav2Vec2ForCTC]:
    """모델을 로컬에 캐싱하거나 다운로드"""
    # 언어별 모델 선택
    model_name = {
        "ko": "kresnik/wav2vec2-large-xlsr-korean",
        "en": "facebook/wav2vec2-base-960h",
    }.get(language)
    
    if model_name is None:
        raise ValueError(f"Unsupported language: {language}")
    
    model_dir = get_project_path('models')
    if model_dir is None:
        raise RuntimeError("Project root not found")
    
    print(f"Loading {language} model from/to: {model_dir}")
    
    processor = Wav2Vec2Processor.from_pretrained(
        model_name, cache_dir=model_dir, force_download=False
    )
    model = Wav2Vec2ForCTC.from_pretrained(
        model_name, cache_dir=model_dir, force_download=False
    )
    
    return processor, model

def save_transcription(text: str, language: str) -> Path:
    """변환된 텍스트를 runs 디렉토리에 저장"""
    runs_dir = get_project_path('runs')
    if runs_dir is None:
        raise RuntimeError("Project root not found")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = runs_dir / f"wav2vec2_transcription_{language}_{timestamp}.txt"
    output_file.write_text(text, encoding="utf-8")
    print(f"Transcription saved to: {output_file}")
    
    return output_file

def extract_audio_from_video(video_path: Path, audio_path: Path):
    """비디오 파일에서 오디오 추출 (MP4 -> WAV)"""
    print(f"Extracting audio from video: {video_path}")
    command = [
        'ffmpeg', '-i', str(video_path), '-vn', '-acodec', 'pcm_s16le', 
        '-ar', '16000', '-ac', '1', str(audio_path)
    ]
    subprocess.run(command, check=True)
    print(f"Audio saved to: {audio_path}")

def transcribe_audio(processor: Wav2Vec2Processor, model: Wav2Vec2ForCTC, 
                    audio_path: Path) -> str:
    """오디오 파일을 텍스트로 변환"""
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    print(f"Transcribing: {audio_path}")
    audio, sr = sf.read(str(audio_path))
    if sr != 16000:
        raise ValueError(f"Expected sampling rate of 16000, but got {sr}")
    
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    
    return postprocess_text(transcription)

def postprocess_text(text: str) -> str:
    """결과 텍스트를 간단히 후처리"""
    text = text.strip()
    text = text.replace("  ", " ")
    return text

def main():
    # 언어 선택 (ko: 한국어, en: 영어)
    language = "en"  # 원하는 언어 선택
    
    # 모델 로드
    processor, model = get_model(language)
    
    # 비디오 파일 경로
    video_path = get_project_path('src/wisper/example3.mp4')
    if video_path is None:
        raise RuntimeError("Video file not found")
    
    # 오디오 파일 경로 (WAV 포맷으로 저장)
    audio_path = get_project_path('src/wisper/extracted_audio.wav')
    
    # 비디오에서 오디오 추출
    extract_audio_from_video(video_path, audio_path)
    
    # 오디오 변환
    transcription = transcribe_audio(processor, model, audio_path)
    
    # 결과 저장 및 출력
    save_transcription(transcription, language)
    print("\nTranscription:")
    print(transcription)

if __name__ == "__main__":
    main()