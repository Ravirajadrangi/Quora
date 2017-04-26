
# coding: utf-8

# In[ ]:

import pandas as pd
from pycorenlp import StanfordCoreNLP 
import TreeBuild as tb
import pickle
import json, os

nlp = StanfordCoreNLP('http://localhost:9000')


# In[ ]:

def read_data(path_to_file):
    df = pd.read_csv(path_to_file)
    print ("Shape of base training File = ", df.shape)
    print("Shape of base training data after cleaning = ", df.shape)
    return df

df_train = read_data("input/train.csv")


# In[ ]:

def _getNLPToks_(rawSentence):
    try:
        output = nlp.annotate(rawSentence, properties={
            'annotators': 'tokenize,ssplit,pos,parse,depparse',
            'outputFormat': 'json'
        })
    except UnicodeDecodeError:
        sentence = unidecode(rawSentence)
        output = nlp.annotate(sentence, properties={
            'annotators': 'tokenize,ssplit,pos,parse,depparse',
            'outputFormat': 'json'
        })
    dependencies = output['sentences'][0]['basicDependencies']
    tokens = output['sentences'][0]['tokens']
    parse = output['sentences'][0]['parse'].split("\n")
    return {'deps':dependencies, 'toks':tokens, 'parse':parse}


# In[ ]:


if __name__ == "__main__":    
    with open('stanfordData_train.nlp', 'wb') as fout:
        count = 0
        for row in df_train.iterrows():
            try:
                q1_stanford = _getNLPToks_(row[1]['question1'])
                q2_stanford = _getNLPToks_(row[1]['question2'])

                tree_1 = tb.tree()
                tree_2 = tb.tree()

                # Generate a tree structure
                tb._generateTree_(q1_stanford['parse'], tree_1)
                tb._generateTree_(q2_stanford['parse'], tree_2)

                # Flip the trees
                tb._flipTree_(tree_1)
                tb._flipTree_(tree_2)

                tmp = {'q1': {
                        'raw': row[1]['question1'],
                        'toks': q1_stanford['toks'],
                        'deps': q1_stanford['deps'],
                        'parse': tree_1
                        },
                       'q2': {
                        'raw': row[1]['question2'],
                        'toks': q2_stanford['toks'],
                        'deps': q2_stanford['deps'],
                        'parse': tree_2                
                        },
                       'id':row[1]['id'],
                       'is_duplicate':row[1]['is_duplicate']
                       }

                pickle.dump(tmp, fout, protocol=pickle.HIGHEST_PROTOCOL)

                tree_1.clear()
                tree_2.clear()
            except:
                print("Failure on row: %d" % count)
                
            count+=1
    
    print("NLP Tree Generation completed!")


# In[ ]:




# In[ ]:




# In[ ]:


