from pocketsphinx import Pocketsphinx
from time import sleep
from os import listdir, path
from subprocess import run, DEVNULL
from fastapi import FastAPI

def transcribe(audiofile):
    return Pocketsphinx()\
        .decode( audio_file = audiofile)\
        .hypothesis()

app = FastAPI()

@app.get("/transcribe/{video_id}")
def transcribe_endpoint(video_id: str):
    run(['ffmpeg', '-y', '-i', './videos/' + video_id + '.mp4', '-acodec', 'pcm_s16le', '-f', 's16le', '-ac', '1', '-ar', '16000', './tmp.raw'], stderr=DEVNULL, stdout=DEVNULL)
    text = transcribe('./tmp.raw')
    return { 'text': text }
