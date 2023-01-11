# unicode, regex, json for text digestion
import unicodedata
import re
import json

# nltk: natural language toolkit -> tokenization, stopwords
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

# pandas dataframe manipulation, acquire script, time formatting
import pandas as pd
import acquire as a
from time import strftime

def basic_clean(string):
    '''
    Takes in a string, makes everything lowercase,
    normalizes unicode characters,removes anything 
    that isn't a letter, number, whitespace or single quote
    '''
    #removes any inconsistencies in unicode character encoding
    #converts the resulting string to the ASCII character set
    #turns the resulting bytes object back into a string
    cleaned_string = unicodedata.normalize('NFKD', string)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore') 
    
    # remove anything that is not a through z, a number, a single quote, or whitespace
    cleaned_string = re.sub(r"[^\w0-9'\s]", '', cleaned_string).lower()
    
    return cleaned_string

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    tokens = tokenizer.tokenize(string, return_str=True)
    return tokens

def stem(string):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    stemmed_string = ' '.join(stems)
    return stemmed_string

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    lemmatized_string = ' '.join(lemmas)
    return lemmatized_string

def remove_stopwords(string, extra_words =[], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # assign our stopwords from nltk into stopword_list
    stopword_list = stopwords.words('english')
    # utilizing set casting, i will remove any excluded stopwords
    stopword_list = set(stopword_list) - set(exclude_words)
    # add in any extra words to my stopwords set using a union
    stopword_list = stopword_list.union(set(extra_words))
    # split our document by spaces
    words = string.split()
    # every word in our document, as long as that word is not in our stopwords
    filtered_words = [word for word in words if word not in stopword_list]
    # glue it back together with spaces, as it was so it shall be
    string_without_stopwords = ' '.join(filtered_words)
    # return the document back
    return string_without_stopwords

def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords,
                                  extra_words=extra_words,
                                  exclude_words=exclude_words)
    
    df['stemmed'] = df['clean'].apply(stem)
    
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df[['title', column,'clean', 'stemmed', 'lemmatized']]