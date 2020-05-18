FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py ./

ENTRYPOINT [ "python", "-u", "./main.py" ]
