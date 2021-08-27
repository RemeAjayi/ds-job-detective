"""
Deploy skill extraction App to Streamlit
Author: Olohireme Ajayi
"""
#imports
import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.initializers import Constant
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm
from keras.layers import Dense,SpatialDropout1D
import contractions
import re 
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
# initializing Stop words libraries
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
#comment spacy imports locally because of incompatibility with numpy 1.19.5
#spacy
import spacy
from spacy.util import filter_spans
from spacy.tokens import Span
from spacy.matcher import Matcher

import en_core_web_sm
nlp = spacy.load(en_core_web_sm)


#clean desc
def clean(desc):
    desc = contractions.fix(desc)
    desc = re.sub("[!@.$\'\'':()]", "", desc)
    return desc

#create pos tags
def tokenize_and_tag(desc):
    tokens = nltk.word_tokenize(desc.lower())
    filtered_tokens = [w for w in tokens if not w in stop_words]
    tagged = nltk.pos_tag(filtered_tokens)
    return tagged

def extract_POS(tagged):
    #pattern 1
    grammar1 = ('''Noun Phrases: {<DT>?<JJ>*<NN|NNS|NNP>+}''')
    chunkParser = nltk.RegexpParser(grammar1)
    tree1 = chunkParser.parse(tagged)

    # typical noun phrase pattern appending to be concatted later
    g1_chunks = []
    for subtree in tree1.subtrees(filter=lambda t: t.label() == 'Noun Phrases'):
        g1_chunks.append(subtree)
    
    #pattern 2
    grammar2 = ('''NP2: {<IN>?<JJ|NN>*<NNS|NN>} ''')
    chunkParser = nltk.RegexpParser(grammar2)
    tree2 = chunkParser.parse(tagged)

    # variation of a noun phrase pattern to be pickled for later analyses
    g2_chunks = []
    for subtree in tree2.subtrees(filter=lambda t: t.label() == 'NP2'):
        g2_chunks.append(subtree)
        
    #pattern 3
    grammar3 = (''' VS: {<VBG|VBZ|VBP|VBD|VB|VBN><NNS|NN>*}''')
    chunkParser = nltk.RegexpParser(grammar3)
    tree3 = chunkParser.parse(tagged)

    # verb-noun pattern appending to be concatted later
    g3_chunks = []
    for subtree in tree3.subtrees(filter=lambda t: t.label() == 'VS'):
        g3_chunks.append(subtree)
        
        
    # pattern 4
    # any number of a singular or plural noun followed by a comma followed by the same noun, noun, noun pattern
    grammar4 = ('''Commas: {<NN|NNS>*<,><NN|NNS>*<,><NN|NNS>*} ''')
    chunkParser = nltk.RegexpParser(grammar4)
    tree4 = chunkParser.parse(tagged)

    # common pattern of listing skills appending to be concatted later
    g4_chunks = []
    for subtree in tree4.subtrees(filter=lambda t: t.label() == 'Commas'):
        g4_chunks.append(subtree)
        
    return g1_chunks, g2_chunks, g3_chunks, g4_chunks

def training_set(chunks):
    '''creates a dataframe that easily parsed with the chunks data '''
    df = pd.DataFrame(chunks)    
    df.fillna('X', inplace = True)
    
    train = []
    for row in df.values:
        phrase = ''
        for tup in row:
            # needs a space at the end for seperation
            phrase += tup[0] + ' '
        phrase = ''.join(phrase)
        # could use padding tages but encoder method will provide during 
        # tokenizing/embeddings; X can replace paddding for now
        train.append( phrase.replace('X', '').strip())

    df['phrase'] = train

    # only returns 10% of each dataframe to be used 
    # Update: only do 50% if running on excel
    return df.phrase

def strip_commas(df):
    '''create new series of individual n-grams'''
    grams = []
    for sen in df:
        sent = sen.split(',')
        for word in sent:
            grams.append(word)
    return pd.Series(grams)

def generate_phrases(desc):
    tagged = tokenize_and_tag(desc)
    g1_chunks, g2_chunks, g3_chunks, g4_chunks = extract_POS(tagged)
    c = training_set(g4_chunks)       
    separated_chunks4 = strip_commas(c)
    # one training corpus with 10% of each POS regex identification
    phrases = pd.concat([training_set(g1_chunks),
                          training_set(g2_chunks), 
                          training_set(g3_chunks),
                          separated_chunks4], 
                            ignore_index = True )
    return phrases

def create_corpus(df):
    """Creates corpus from feature column, which is a pandas series"""
    corpus=[]
    for phrase in tqdm(df):
        words=[word.lower() for word in word_tokenize(phrase) if(word.isalpha()==1)]
        corpus.append(words)
    return corpus

def create_padded_inputs(corpus):
    """Create padded sequences of equal lenght as input to LSTM"""
    MAX_LEN=20
    tokenizer_obj=Tokenizer()
    tokenizer_obj.fit_on_texts(corpus)
    sequences=tokenizer_obj.texts_to_sequences(corpus)

    phrase_pad=pad_sequences(sequences,maxlen=MAX_LEN,truncating='post',padding='post')
    return phrase_pad

def get_predictions(desc):
    #clean
    desc = clean(desc)
    #load model
    model = tf.keras.models.load_model('models/lstm_skill_extractor.h5')
    #tokenize and convert to phrases
    phrases = generate_phrases(desc)
    #preprocess unseen data
    corpus=create_corpus(phrases)
    corpus_pad = create_padded_inputs(corpus)
    #get predicted classes
    predictions = (model.predict(corpus_pad) > 0.65).astype('int32')
    #return predicted skills as list
    out = pd.DataFrame({'Phrase':phrases, 'Class':predictions.ravel()})
    skills = out.loc[out['Class'] == 1]
    return skills['Phrase'].tolist()

def get_predictions_excel(filename):
    """description column must be titled Job Desc"""
    df = pd.read_csv(filename)
    df['Extracted skills'] = df['Job Description'].apply(lambda x: get_predictions(x))
    
    return df.to_csv('extracted.csv')

    #throw error if column name does not exist or file format is wrong

#comment spacy imports locally because of incompatibility with numpy 1.19.5
#methods for rule-based model
def get_left_span(tok, label='', include=True):
    offset = 1 if include else 0
    idx = tok.i
    while idx > tok.left_edge.i:
        if tok.doc[idx - 1].pos_ in ('NOUN', 'PROPN', 'ADJ', 'X'):
            idx -= 1
        else:
            break
    return label, idx, tok.i+offset

def get_conjugations(tok):
    new = [tok]
    while new:
        tok = new.pop()
        yield tok
        for child in tok.children:
            if child.dep_ == 'conj':
                new.append(child)

EXP_TERMS = ['experience']
def extract_adp_conj_experience(doc, label='EXPERIENCE'):
    for tok in doc:
        if tok.lower_ in EXP_TERMS:
            for child in tok.rights:
                if child.dep_ == 'prep':
                    for obj in child.children:
                        if obj.dep_ == 'pobj':
                            for conj in get_conjugations(obj):
                                yield get_left_span(conj, label)

def get_extractions(examples, *extractors):
    # Could use context instead of enumerate
    doc = nlp(examples, disable=['ner'])
    for ent in filter_spans([Span(doc, start, end, label) for extractor in extractors for label, start, end in extractor(doc)]):
        sent = ent.root.sent
        yield ent.text


def list_skills(examples, *extractors):
    return list(get_extractions(examples, *extractors))


header = st.container()

with header:
    st.title('Skill Extraction with LSTM')

st.text('A machine learning model to extract skills from job descriptions.')
st.text('You can use it by typing a job description or pasting one from your favourite job board.')


with st.form(key='my_form'):
	desc = st.text_area(label='Enter a Job Description', height=300)
	submit = st.form_submit_button(label='Submit')

if submit:
    skills_1 = get_predictions(desc)
    skills_2 = list_skills(desc, extract_adp_conj_experience)
    st.caption(f'Here are your skills')

    col1, col2 = st.columns(2)

    col1.header("LSTM")
    col1.table(skills_1)

#comment spacy imports locally because of incompatibility with numpy 1.19.5
    col2.header("Rule-Based")
    col2.table(skills_2)