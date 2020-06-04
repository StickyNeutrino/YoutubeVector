from pymongo import MongoClient, errors
from pocketsphinx import AudioFile, get_model_path, get_data_path, Pocketsphinx
from time import sleep
from os import listdir, path
from subprocess import run, DEVNULL

client = MongoClient(
    'mongodb://mongo:27017/',
    username = "root",
    password = "example")

videos = client.youtube.videos
transcripts = client.youtube.transcripts

def transcribe(audiofile):
    return Pocketsphinx()\
        .decode( audio_file = audiofile)\
        .hypothesis()

def videoExists(id):
    id + '.mp4' in listdir('./videos')

def transcribed(id):
    transcripts.find({'id': id}, {'id': 1}).limit(1).count() != 0
    #do simple cache here
while 1:
    for video in videos.find({}, {'yt_videoid': 1}):
        id = video['yt_videoid']
        if not transcribed(id) \
        and videoExists(id):
            try:
                run(['ffmpeg', '-y', '-i', './videos/' + id + '.mp4', '-acodec', 'pcm_s16le', '-f', 's16le', '-ac', '1', '-ar', '16000', './tmp.raw'], stderr=DEVNULL, stdout=DEVNULL)
                text = transcribe('./tmp.raw')
                videos.update_one({'id': video['id']} , {'$set': {'text': text}})
            except:
                continue
    sleep(10)
