import feedparser
from pymongo import MongoClient
from time import sleep
import requests

print('connecting')
client = MongoClient(
    'mongodb://mongo:27017/',
    username="root", password="example")
print('connected')
videos = client.youtube.videos

while 1:
    print('starting')
    with open('./channel_ids', 'r') as channel_ids:
        for id in channel_ids:
            raw = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=' + id)
            for entry in raw['entries']:
                if videos.find({'id': entry["id"]}).limit(1).count() == 0:
                    print('New:', entry['id'])
                    videos.insert(entry)
                    requests.get('http://pipeline:8000/video2vec/' + entry['yt_videoid'])
                    #index video jn
    print('sleeping')
    sleep( 60 )
