from pymongo import MongoClient, errors
from pocketsphinx import AudioFile, get_model_path, get_data_path, Pocketsphinx
from time import sleep
from os import listdir, path
from subprocess import run

print('started')

client = MongoClient(
    'mongodb://mongo:27017/',
    username = "root",
    password = "example")
print('connected to db')

videos = client.youtube.videos

def transcribe(audiofile):
    return Pocketsphinx()\
        .decode( audio_file = audiofile)\
        .hypothesis()

skipList = []
while 1:
    print("Starting")
    for video in videos.find({'text': None}):
        id = video['yt_videoid']
        if id + '.mp4' in listdir('./videos') \
        and id not in skipList:
            sleep(5)
            print('transcribing:', id)
            try:
                videos.update_one({'id': video['id']} , {'$set': {'text': '*'}})
                run(['ffmpeg', '-y', '-i', './videos/' + id + '.mp4', '-acodec', 'pcm_s16le', '-f', 's16le', '-ac', '1', '-ar', '16000', './tmp.raw'])
                text = transcribe('tmp.raw')
                videos.update_one({'id': video['id']} , {'$set': {'text': text}})
                print(text)
            except:
                print('skipping:', id)
                skipList.append(id)
    print('sleeping')
    sleep(10)
