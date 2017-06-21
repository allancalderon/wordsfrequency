from nltk.corpus import stopwords  
from nltk.stem import SnowballStemmer

import re
import sys
from operator import itemgetter
from tokenization import unigrams_and_bigrams, process_tokens

import regex

class WordsFrequency(object):

    def __init__(self, language='english',  collocations=True):
        self.list_stopwords = []
        self.__collocations = collocations
        #TODO: verify supported languages of NKTL library (stopwords and stem libraries)
        self.__supported_languages = ['english','spanish'] 
        self.__language = 'english' if (language not in self.__supported_languages) else language
        self.__collocation = collocations
        self.__sentences = ''
        self.__words = None
        self.__words_stemmed = None
        self.__words_frequency = None
        
    def get_sentences(self):
        return self.__sentences
    
    def get_words(self):
        return self.__words
    
    def get_language(self):
        return self.__language
    
    def get_words_stemmed(self):
        return self.__words_stemmed
    
    def get_words_frequency(self):
        return self.__words_frequency
    
    def __words_process(self, text, new_stopwords):
        #remove all non latin characteres
        self.__sentences = regex.sub("ur'[^\p{Latin}]'", "u''", text)
        #define flags and regexp
        flags = (re.UNICODE if sys.version < '3' and ((type(self.get_sentences()) is unicode) or (type(self.get_sentences()) is locale)) else 0)
        regexp = r"\w[\w']+"
        #We only want to work with lowercase for the comparisons
        self.__sentences = self.get_sentences().lower()
        #get words
        words = re.findall(regexp, self.get_sentences(), flags)
        # remove stopwords
        self.list_stopwords = set(stopwords.words(self.get_language()))
        self.list_stopwords.update(new_stopwords)
        words = [word for word in words if word.lower() not in self.list_stopwords]
        #remove numbers
        words = [word for word in words if not word.isdigit()]
        return words 
    
    def __words_process_stemmed(self):
        stemmer = SnowballStemmer(self.get_language())
        words_stemmed = []
        for item in self.get_words():
            words_stemmed.append(stemmer.stem(item))
        return words_stemmed
    
    def __words_process_frequency(self):
        if self.__collocations:
            word_counts = unigrams_and_bigrams(self.get_words_stemmed())
        else:
            word_counts, _ = process_tokens(self.get_words_stemmed())
        item1 = itemgetter(1)
        words_frequency = sorted(word_counts.items(), key=item1, reverse=True)
        return words_frequency
            
    def process_text(self, text = '', new_stopwords=[]):
        self.__words = self.__words_process(text, new_stopwords)
        self.__words_stemmed = self.__words_process_stemmed()
        self.__words_frequency = self.__words_process_frequency()
        return self.get_words_frequency()

#Download the spanish stopwords first with nltk.download()
wf = WordsFrequency(language='spanish')
words_frequency = wf.process_text("Calidad precio muy buenos. Huawei se está luciendo es ligero. Rápido y está muy bien para un uso normal de un móvil siempre que no sea para usos más recurrentes o frecuentes. Este dispositivo es perfecto para uso normal como redes sociales. WhatsApp. Alguna app y de más.")
print(words_frequency)
print(wf.get_words_stemmed())
print(wf.get_words())
print(wf.get_sentences())
