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

def transcribe(audiofile):
    return Pocketsphinx()\
        .decode( audio_file = audiofile)\
        .hypothesis()

skipList = []
def run():
    for video in videos.find({'text': None}):
        id = video['yt_videoid']
        if id + '.mp4' in listdir('./videos') \
        and id not in skipList:
            try:
                run(['ffmpeg', '-y', '-i', './videos/' + id + '.mp4', '-acodec', 'pcm_s16le', '-f', 's16le', '-ac', '1', '-ar', '16000', './tmp.raw'], stderr=DEVNULL, stdout=DEVNULL)
                text = transcribe('./tmp.raw')
                videos.update_one({'id': video['id']} , {'$set': {'text': text}})
            except:
                skipList.append(id)


while 1:
    run()
    sleep(10)
