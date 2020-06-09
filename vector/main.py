import os
import gensim.models as g
import codecs
from nltk.tokenize import word_tokenize
import nltk
from pymongo import MongoClient
import random
corpus = []
import pysrt

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

def test_model(test_data):
    #parameters
    model_path="d2v.model"
    #load model
    model = g.Doc2Vec.load(model_path)
    test_docs = [word_tokenize(doc) for doc in test_data]

    #From doc2vec page
    # Pick a random document from the test corpus and infer a vector from the model
    doc_id = random.randint(0, len(test_docs) - 1)
    inferred_vector = model.infer_vector(test_docs[doc_id])
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

    # Compare and print the most/median/least similar documents from the train corpus
    print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(corpus[doc_id])))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 1), ('SECOND', 2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(corpus[sims[index][0]])))

client = MongoClient(
    'mongodb://mongo:27017/',
    username="root", password="example")

transcripts = client.youtube.transcripts

corpus = []
for transcript in os.listdir('./transcripts'):
    text = ''
    for sub in pysrt.open('./transcripts/' + transcript):
        text += sub.text
    corpus.append(text)

train_model(corpus)
for i in range(5):
    test_model(corpus)
