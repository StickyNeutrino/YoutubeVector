from os import listdir
from fastapi import FastAPI

def videoExists(id):
    id + '.mp4' in listdir('./videos')

def download(id):
    from pytube import YouTube
    if not videoExists(id):
        try:
            YouTube('https://youtu.be/' + id) \
            .streams \
            .filter(progressive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first() \
            .download(output_path='./videos', filename=id)
            return True
        except:
            return False
    return True


app = FastAPI()

@app.get("/download/{video_id}")
def download_endpoint(video_id: str):
    return { 'success': download(video_id) }
