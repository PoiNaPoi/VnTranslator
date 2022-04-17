import subprocess
import sys

Library = ['opencv-python==4.5.4.60', 'Pillow', 'PyQt5', 'easyocr==1.4.1', 'unidic-lite', 'cutlet', 'deep_translator']

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

subprocess.check_call([sys.executable, "installFile\get-pip.py"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

for lib in Library:
    install(lib)