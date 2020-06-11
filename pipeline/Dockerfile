FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py ./

RUN mkdir ./videos

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
