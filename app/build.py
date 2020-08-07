#Basic
import time
import pandas as pd
import pickle
from scipy import sparse #Sparsed Vectorizers
import scipy.stats as ss 
from scipy.sparse import hstack

#Vectorizers
from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.feature_extraction.text import TfidfVectorizer as TF

#MNB Classifier Modelling
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.utils import resample
import numpy as np

def sampler(df, thresh=22700):
    """
    Undersamples/Upsamples labels to a given threshold
    """
    f_df={k:df[df['Flair']==k] for k in set(df['Flair'])}
    train_df=pd.concat([resample(data[100:], n_samples=22700, replace=True, random_state=123) for data in f_df.values()])
    return train_df

if __name__ == "__main__":

    #Target Paths
    VEC_PATH = 'tfidf.pickle'
    MODEL_PATH = 'model.pickle'

    #Load Data
    DATA_PATH = 'data.csv'
    df=pd.read_csv(open(DATA_PATH), encoding='utf-8').dropna()

    #UNDERSAMPLE
    train_df = sampler(df)
    
    #Feature Extractor
    cv=TF(sublinear_tf=True,min_df=10, encoding='latin-1',ngram_range=(1,1),stop_words='english', analyzer='word', max_features=6150)
    cv.fit(df['Title']+' '+df['Text'])
    pickle.dump(model, open(VEC_PATH, 'wb'))

    #Build Model
    model= MNB()
    train_data=hstack((cv.transform(train_df['Title']),cv.transform(train_df['Text'])))
    model.fit(train_data, train_df['Flair'])
    pickle.dump(model, open(MODEL_PATH, 'wb'))



