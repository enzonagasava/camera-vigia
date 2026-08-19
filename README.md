# Camera App

Aplicação de captura e processamento de vídeo utilizando Python e OpenCV.

## Requisitos

- Python 3.11+
- Webcam
- OpenCV

## Instalação

Crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python main.py

## Comando para setar brilho da webcam
v4l2-ctl -d /dev/video3 --set-ctrl=brightness=300

