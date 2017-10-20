# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

information: http://textminingonline.com/dive-into-nltk-part-ii-sentence-tokenize-and-word-tokenize
"""

from nltk import sent_tokenize, word_tokenize, pos_tag
import nltk

sentence = "Set my alarm to 5am."
"""
Another equivalent call method like the following:
>>> from nltk.tokenize import TreebankWordTokenizer
>>> tokenizer = TreebankWordTokenizer()
>>> tokenizer.tokenize(“this’s a test”)
[‘this’, “‘s”, ‘a’, ‘test’]

Calls TreebankWordTokenizer

Except the TreebankWordTokenizer, there are other alternative word tokenizers, such as PunktWordTokenizer and WordPunktTokenizer.

PunktTokenizer splits on punctuation, but keeps it with the word:

>>> from nltk.tokenize import PunktWordTokenizer
>>> punkt_word_tokenizer = PunktWordTokenizer()
>>> punkt_word_tokenizer.tokenize(“this’s a test”)
[‘this’, “‘s”, ‘a’, ‘test’]

WordPunctTokenizer splits all punctuations into separate tokens:

>>> from nltk.tokenize import WordPunctTokenizer
>>> word_punct_tokenizer = WordPunctTokenizer()
>>> word_punct_tokenizer.tokenize(“This’s a test”)
[‘This’, “‘”, ‘s’, ‘a’, ‘test’]

You can choose any word tokenizer in nltk for your using purpose. 
"""
tokens = word_tokenize(sentence)
"""
>>> nltk.batch_pos_tag([[‘this’, ‘is’, ‘batch’, ‘tag’, ‘test’], [‘nltk’, ‘is’, ‘text’, ‘analysis’, ‘tool’]])
[[(‘this’, ‘DT’), (‘is’, ‘VBZ’), (‘batch’, ‘NN’), (‘tag’, ‘NN’), (‘test’, ‘NN’)], [(‘nltk’, ‘NN’), (‘is’, ‘VBZ’), (‘text’, ‘JJ’), (‘analysis’, ‘NN’), (‘tool’, ‘NN’)]]
"""
tagged_tokens = pos_tag(tokens)
print(tagged_tokens)

nltk.help.upenn_tagset('CD')


"""
Training a POS Tagger
"""
from nltk.corpus import treebank
from nltk.tag import tnt
#Fo Saving POS Taggers
import pickle

print(len(treebank.tagged_sents()))
train_data = treebank.tagged_sents()[:3000]
test_data = treebank.tagged_sents()[3000:]
print(train_data[0])

tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(train_data)
tnt_pos_tagger.evaluate(test_data)

#Save POS Tagger as pickle-file
file_1 = open('tnt_treebank_pos_tagger.pickle', 'wb')
pickle.dump(tnt_pos_tagger, file_1)
file_1.close()

file=open('tnt_treebank_pos_tagger.pickle', 'rb')
tnt_pos_tagger = pickle.load(file)
file.close()

#reopen tagger
#tnt_tagger.tag(nltk.word_tokenize(“this is a tnt treebank tnt tagger”))

"""Stemmer and Lemmer"""

from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
porter_stemmer.stem(‘maximum’)

from nltk.stem.lancaster import LancasterStemmer
lancaster_stemmer = LancasterStemmer()
lancaster_stemmer.stem(‘maximum’)

from nltk.stem import SnowballStemmer
snowball_stemmer = SnowballStemmer(“english”)
snowball_stemmer.stem(‘maximum’)

from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
wordnet_lemmatizer.lemmatize(‘dogs’)

#lemmatize(is, pos=’n’)
#So you need specified the pos for the word like these:
wordnet_lemmatizer.lemmatize(‘is’, pos=’v’)
#-->u’be’

from nltk.tag.stanford import POSTagger

english_postagger = POSTagger('models/english-bidirectional-distsim.tagger', 'stanford-postagger.jar')

english_postagger.tag('this is stanford postagger in nltk for python users'.split())














