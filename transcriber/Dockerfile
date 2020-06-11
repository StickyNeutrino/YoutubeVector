FROM python

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y swig libpulse-dev libasound2-dev ffmpeg
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py ./

RUN mkdir ./videos

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
