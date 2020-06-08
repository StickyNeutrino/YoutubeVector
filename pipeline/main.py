from pymongo import MongoClient
from fastapi import FastAPI
from time import sleep
import requests

client = MongoClient(
    'mongodb://mongo:27017/',
    username="root", password="example")

app = FastAPI()

@app.get("/doc2vec/{video_id}")
def pipeline_endpoint(video_id: str):
    requests.get('http://downloader:8000/download/' + video_id)
    resp = requests.get('http://transcriber:8000/transcribe/' + video_id)
    text = resp.json().text
    print(text)
    return { 'success': True }
