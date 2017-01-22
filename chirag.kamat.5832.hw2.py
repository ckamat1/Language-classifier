# coding: utf-8
import codecs
import operator
from math import log

classes = ['en','de','nl','sv'] #List of languages supported for identification
alphabet = set()
texts = {}

for lang in classes:
    texts[lang] = [line.strip() for line in codecs.open(lang, 'r',encoding='utf-8')][0]
    alphabet |= {unigram for unigram in texts[lang]}

bigram_base = {} #dictionary of dictionaries containing bigram counts for each language
unigram_base = {} #dictionary of dictionaries containing unigram counts for each language


'''Following code computes the bigram and unigram count
    for each of the 4 languages'''

for lang,text in texts.iteritems():
    bigram_counts = {}
    unigram_counts = {}
    for c1,c2 in zip(text,text[1:]):
        bigram = c1 + c2
        if not bigram_counts.has_key(bigram):
            bigram_counts[bigram] = 1
        else:
            bigram_counts[bigram] += 1
        if not unigram_counts.has_key(c1):
            unigram_counts[c1] = 1
        else:
            unigram_counts[c1] += 1
        bigram_base.update({lang:bigram_counts})
        unigram_base.update({lang:unigram_counts})

'''Classify method will loop through the input string,
compute the log probabilities of each bigram and sum them'''

def classify(unigram_base,bigram_base,classes,sample_string):
    sample_string = ' ' + sample_string
    probs = {}
    total_probs = {}
    for item in classes:
        probs.update({item:{}})
        total_probs.update({item:0})
    for c1,c2 in zip(sample_string,sample_string[1:]):
        bigram = c1 + c2
        for lang in classes:
            probs[lang][bigram]  =  log (float(bigram_base[lang].get(bigram,0.00) + 1.00)/(unigram_base[lang].get(c1,0.00) + 32.00)) #computing log probabilities for bigrams
            total_probs[lang] += probs[lang][bigram]# Computing the sum of all the bigrams in the sample string
    bestclass = max(total_probs.iteritems(),key = operator.itemgetter(1))[0]
    return (bestclass,total_probs)

print classify(unigram_base,bigram_base, classes, u'this is a very short text') #english
print classify(unigram_base,bigram_base, classes, u'dies ist ein sehr kurzer text') #german
print classify(unigram_base,bigram_base, classes, u'dit is een zeer korte tekst') #dutch
print classify(unigram_base,bigram_base, classes, u'detta är en mycket kort text') #swedish

# print alphabet
# input_list = [u'I love natural language processing',u'Ich liebe die Verarbeitung natürlicher Sprache',
#               u'Ik hou van de natuurlijke taalverwerking',u'Jag älskar naturligt språk']
#
# for item in input_list:
#     print classify(unigram_base,bigram_base,classes,item)