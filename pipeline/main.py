from fastapi import FastAPI
from time import sleep
import requests

app = FastAPI()

@app.get("/video2vec/{video_id}")
def pipeline_endpoint(video_id: str):
    requests.get('http://downloader:8000/caption/' + video_id)
    return
    ''' NOTE: CMU Spynx works but too slow to build index
    transcript = transcripts.find_one({'id': video_id})
    text = ''
    if not transcript:
        resp = requests.get('http://transcriber:8000/transcribe/' + video_id)
        value = resp.json()
        transcripts.insert({ 'id': video_id, 'value': value})
        text = value['text']
    else:
        text = transcript['value']['text']

    print(text)
    return { 'success': True }
    '''
