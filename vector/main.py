import os
import gensim.models as g
import codecs
from nltk.tokenize import word_tokenize

def train_model(train_data):
    #doc2vec parameters
    vector_size = 300
    min_count = 2
    train_epoch = 50
    dm = 0

    #output model
    saved_path = "d2v.model"

    #train doc2vec model
    docs = [g.doc2vec.TaggedDocument(doc, [i]) for i, doc in enumerate(train_data)]
    model = g.Doc2Vec(docs, size=vector_size, min_count=min_count, dm=dm, dbow_words=1, dm_concat=1, epochs=train_epoch)

    #save model
    model.save(saved_path)

def test_model(test_data):
    #parameters
    model="d2v.model"
    output_file="test_vectors.txt"

    #load model
    m = g.Doc2Vec.load(model)
    test_docs = [word_tokenize(doc) for doc in test_data]

    #infer test vectors
    output = open(output_file, "w")
    for d in test_docs:
        output.write( " ".join([str(x) for x in m.infer_vector(d)]) + "\n" )
    output.flush()
    output.close()