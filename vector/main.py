import os
import gensim.models as g


def train_model(train_data):
    #doc2vec parameters
    vector_size = 300
    window_size = 15
    min_count = 2
    sampling_threshold = 1e-5
    negative_size = 5
    train_epoch = 100
    dm = 0
    worker_count = 1 #number of parallel processes

    #output model
    saved_path = "model"

    #train doc2vec model
    docs = g.doc2vec.TaggedLineDocument(train_data)
    model = g.Doc2Vec(docs, size=vector_size, window=window_size, min_count=min_count, sample=sampling_threshold, workers=worker_count, hs=0, dm=dm, negative=negative_size, dbow_words=1, dm_concat=1, iter=train_epoch)

    #save model
    model.save(saved_path)