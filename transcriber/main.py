from pymongo import MongoClient, errors
import pocketsphinx
from time import sleep
from os import listdir

print('started')
exit()
client = MongoClient(
    'mongodb://mongo:27017/',
    username = "root",
    password = "example")
print('connected to db')

videos = client.youtube.video

skipList = []
while 1:
    print("Starting")
    for video in videos.find():
        id = video['yt_videoid']
        if id + '.mp4' in listdir('./videos') \
        and id not in skipList:
            sleep(5)
            print('transcribing:', id)
            try:
                print('TODO')
            except:
                print('skipping:', id)
                skipList.append(id)
    print('sleeping')
    sleep(60 * 17)
