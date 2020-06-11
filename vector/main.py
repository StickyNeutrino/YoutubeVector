import os
import gensim.models as g
import codecs
from nltk.tokenize import word_tokenize
import nltk
import random
corpus = []
import pysrt
from fastapi import FastAPI
import requests

nltk.download('punkt')

def train_model(train_data):
    #doc2vec parameters
    vector_size = 50
    min_count = 2
    train_epoch = 50
    dm = 0

    #output model
    saved_path = "d2v.model"

    #train doc2vec model
    docs = [g.doc2vec.TaggedDocument(word_tokenize(doc), [i]) for i, doc in enumerate(train_data)]
    model = g.Doc2Vec(docs, size=vector_size, min_count=min_count, dm=dm, dbow_words=1, dm_concat=1, epochs=train_epoch)

    #save model
    model.save(saved_path)

def similar(id):
    text = ''
    for sub in pysrt.open('./transcripts/' + id + '.srt'):
        text += sub.text + ' '
    #parameters
    model_path="d2v.model"
    #load model
    model = g.Doc2Vec.load(model_path)

    inferred_vector = model.infer_vector(word_tokenize(text))
    sims = model.docvecs.most_similar([inferred_vector], topn=4)

    lines = open("./trained_ids.txt").readlines()
    print(lines)
    print(sims)
    return {"one": lines[sims[0][0]],"two": lines[sims[1][0]],"three": lines[sims[2][0]]}

def train():
    corpus = []
    trained_ids = []
    for transcript in os.listdir('./transcripts'):
        text = ''
        for sub in pysrt.open('./transcripts/' + transcript):
            text += sub.text + ' '
        corpus.append(text)
        trained_ids.append(transcript.split('.')[0])

    train_model(corpus)
    id_file = open('./trained_ids.txt', 'w')
    for id in trained_ids:
        id_file.write(id + '\n')
    id_file.close()

app = FastAPI()

@app.get("/train/")
def train_endpoint():
    train()
    return { 'ok': True }

@app.get("/similar/{video_id}")
def similar_endpoint(video_id: str):
    print( requests.get('http://downloader:8000/caption/' + video_id).json())
    return similar(video_id)
