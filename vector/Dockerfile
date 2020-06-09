FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY main.py ./

RUN mkdir ./transcripts

ENTRYPOINT [ "python", "-u", "./main.py" ]
