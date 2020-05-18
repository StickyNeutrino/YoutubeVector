from pymongo import MongoClient, errors
from pytube import YouTube
from time import sleep
from os import listdir

print('started')
sleep(7)

client = MongoClient(
    'mongodb://mongo:27017/',
    username = "root",
    password = "example")
print('connected to db')

videos = client.youtube.videos

skipList = []
while 1:
    print("Starting")
    for video in videos.find():
        id = video['yt_videoid']
        if id + '.mp4' not in listdir('./videos') \
        and id not in skipList:
            sleep(5)
            print('downloading:', id)
            try:
                YouTube('https://youtu.be/' + id) \
                .streams \
                .filter(progressive=True, file_extension='mp4') \
                .order_by('resolution') \
                .desc() \
                .first() \
                .download(output_path='./videos', filename=id)
            except:
                print('skipping:', id)
                skipList.append(id)
    print('sleeping')
    sleep(60 * 17)
