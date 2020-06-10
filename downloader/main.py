from os import listdir
from fastapi import FastAPI
from pytube import YouTube

def videoExists(id):
    id + '.mp4' in listdir('./videos')

def captionExists(id):
    id + 'srt' in listdir('./transcripts')

def downloadVideo(id):
    if not videoExists(id):
        try:
            YouTube('https://youtu.be/' + id) \
            .streams \
            .filter(progressive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first() \
            .download(output_path='./videos', filename=id)
        except:
            return False
    return True

def downloadCaption(id):
    if not captionExists(id):
        try:
            captions = YouTube('https://youtu.be/' + id) \
            .captions['en'] \
            .generate_srt_captions()

            file = open('/usr/src/app/transcripts/' + id + '.srt', mode='w')
            file.write(captions)
            file.close()
        except:
            return False
    return True

app = FastAPI()

@app.get("/video/{video_id}")
def download_endpoint(video_id: str):
    return { 'video': downloadVideo(video_id) }

@app.get("/caption/{video_id}")
def caption_endpoint(video_id: str):
    return { 'caption': downloadCaption(video_id) }
