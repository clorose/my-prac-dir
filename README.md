# Pyenv 및 Poetry 설정 가이드 + Docker 실행

이 문서는 Python 3.11 환경에서 PyTorch 설치를 위한 Pyenv 및 Poetry 설정과 Docker 컨테이너 실행 과정을 설명합니다.

---

## 1. Pyenv 및 Poetry 설치
Pyenv와 Poetry를 `pipx`를 사용해 설치합니다.

```bash
pipx install pyenv
pipx install poetry
```

---

## 2. Pyenv로 Python 3.11 설치
PyTorch 호환성을 위해 Python 3.11을 설치합니다.

```bash
pyenv install 3.11
```

---

## 3. Pyenv로 Python 버전 설정
현재 디렉토리에서 Python 3.11을 기본 버전으로 사용하도록 설정합니다.

```bash
pyenv local 3.11
```

설정 확인:

```bash
python --version
# 결과: Python 3.11.x
```

---

## 4. Poetry로 가상환경 생성
Poetry를 사용해 Python 3.11 기반의 가상환경을 생성합니다.

```bash
poetry env use python3.11
```

---

## 5. Pyenv Local 설정 해제
Python 버전 설정을 디렉토리 단위로 유지하지 않으려면 `pyenv local`을 해제합니다.

```bash
pyenv local --unset
```

---

## Docker 컨테이너 실행

### 1. Docker Compose 실행
프로젝트 디렉토리에 제공된 **`docker-compose.yml`** 파일을 사용하여 개발 환경 컨테이너를 실행합니다.

```bash
docker compose up dev
```

### 2. 컨테이너 접속
컨테이너가 성공적으로 실행되면 아래 명령어로 컨테이너 내부에 접속할 수 있습니다.

```bash
docker exec -it <컨테이너 이름> bash
```

예시:

```bash
docker exec -it yolo-dev-1 bash
```