from os import listdir
from fastapi import FastAPI

def videoExists(id):
    id + '.mp4' in listdir('./videos')

def captionExists(id):
    id + 'srt' in listdir('./transcripts')

def download(id):
    from pytube import YouTube

    response = { 'caption': True, 'video': True}

    if not captionExists(id): 
        try:
            captions = YouTube('https://youtu.be/' + id) \
            .captions['en'] \
            .generate_srt_captions()

            file = open('/usr/src/app/transcripts/' + id + '.srt', mode='w')
            file.write(captions)
            file.close()

        except:
            response['caption'] = False

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
            response['video'] = False
    return response


app = FastAPI()

@app.get("/download/{video_id}")
def download_endpoint(video_id: str):
    return download(video_id)
