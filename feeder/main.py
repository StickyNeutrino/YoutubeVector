import feedparser
from time import sleep
import requests


def download(id):
    requests.get('http://pipeline:8000/video2vec/' + id)

while 1:
    print('starting')
    with open('./channel_ids', 'r') as channel_ids:
        for id in channel_ids:
            raw = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=' + id)
            for entry in raw['entries']:
                download(entry['yt_videoid'])
    print('sleeping')
    sleep( 60 )
