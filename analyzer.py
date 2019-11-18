from textblob import TextBlob
from textblob.utils import tree2str, filter_insignificant
import nltk
import sys
import time

start_time = time.time()

def compound(text):
    converted = [] #will contain the converted strings
    blob = TextBlob(text)
    for sentence in blob.sentences:
        for index, tag in enumerate(sentence.tags):
            if index > 0 and sentence.tags[index-1][1] == tag[1]:
                if len(converted) > 0:
                    converted.pop()
                tup = (sentence.tags[index-1][0] + ' ' + tag[0], tag[1])
                converted.append(tup)
            else:
                tup = (tag[0], tag[1])
                converted.append(tup)


    return converted

def get_first_index_of(tag, all_tags):
    index = 0
    for tag_temp in all_tags:
        if tag in tag_temp[1]:
            return index
        else:
            index += 1
    return

def get_last_index_of(tag, all_tags):
    index = len(all_tags)
    for tag_temp in reversed(all_tags):
        if tag in tag_temp[1]:
            return index
        else:
            index -= 1
    return

def get_verbs(tags):
    ''' Finds the verbs'''
    verbs = []
    for tag in tags:
        if 'VB' in tag[1] or 'RP' in tag[1] and 'PRP' not in tag[1]:
            verbs.append(tag)
    return verbs

def get_determiner(verbs, all_tags):
    ''' Finds the Determiner before the provided verb'''
    if len(verbs) > 0:
        verb = verbs[len(verbs) - 1]
        index = all_tags.index(verb)
        tags = all_tags[index+1:]
        nouns = []
        for tag in tags:
            if 'DT' in tag[1]:
                return tag

def noun_before_verbs(verbs, all_tags):
    ''' Finds the Noun before the provided verb'''
    if len(verbs) > 0:
        verb = verbs[0]
        index = converted_tags.index(verb)
        tags = all_tags[:index]

        nouns = []
        for tag in tags:
            if 'NN' in tag[1] or 'PRP' in tag[1] or 'EX' in tag[1] or 'CC' in tag[1]:
                nouns.append(tag)
        return nouns

def prep_after_verb(verb, all_tags):
    ''' Finds the Preposition after the provided verb'''
    if len(verbs) > 0:
        verb = verbs[0]
        index = converted_tags.index(verb)
        tags = all_tags[index+1:]

        preps = []
        for tag in tags:
            if 'IN' in tag[1]:
                preps.append(tag)
        return preps


def noun_after_verb(verbs, all_tags):
    ''' Finds the Noun after the provided verb'''
    if len(verbs) > 0:
        verb = verbs[len(verbs) - 1]
        index = all_tags.index(verb)
        tags = all_tags[index+1:]
        first_index = get_first_index_of('NN',tags)
        tags = tags[first_index:]
        # return tags
        nouns = []
        for tag in tags:
            if 'NN' in tag[1]: # or 'IN' in tag[1]:
                nouns.append(tag)
        return nouns

def adj_after_verb(verbs, all_tags):
    ''' Finds the adjective after the provided verb'''
    if len(verbs) > 0:
        verb = verbs[len(verbs) - 1]
        index = all_tags.index(verb)
        tags = all_tags[index+1:]
        # return tags
        adjs = []
        for tag in tags:
            if 'JJ' in tag[1] or 'RB' in tag[1]:
                adjs.append(tag)
        return adjs


text = '''
The engineers at Apple train Machine Learning models on large, transcribed datasets in order to create efficient speech recognition models for Siri. These models are trained with highly diverse datasets that comprise of the voice samples of a large group of people. This way, Siri is able to cater to various accents.
'''

texts = [
    "I'm sad.",
    "Menan is eating.",
    "Lions are beautiful.",
    "Sri Lanka is racist.",
    "Canada is cold.",
]

texts2 = [
    "My brother and I went to the mall last night.",
    "This new laptop computer has already crashed twice.",
    "I cannot drink warm milk.",
    "A day without sunshine is like night.",
    "Only the mediocre are always at their best.",
    "Reality continues to ruin my life.",
]
texts3 = [
    "My brother and I went to the mall last night.",
    "This new laptop computer has already crashed twice.",
    "I cannot drink warm milk.",
    "A day without sunshine is like night.",
    "Only the mediocre are always at their best.",
    "Reality continues to ruin my life.",
]
texts4 = [
    "The engineers at Apple train Machine Learning models on large, transcribed datasets in order to create efficient speech recognition models for Siri. ",
    "These models are trained with highly diverse datasets that comprise of the voice samples of a large group of people.",
    "This way, Siri is able to cater to various accents.",
]

for aText in texts4:
    converted_tags = compound(aText)
    verbs = get_verbs(converted_tags)
    subjects = noun_before_verbs(verbs, converted_tags)
    objects = noun_after_verb(verbs, converted_tags)
    preposition = prep_after_verb(verbs, converted_tags)
    determiner = get_determiner(verbs, converted_tags)
    adj = adj_after_verb(verbs, converted_tags)

    print(aText)
    print('-----------------------------------------')
    print(converted_tags)
    print('Verbs: \t\t\t', verbs)
    print('Subjects:\t\t', subjects)
    print('Objects:\t\t', objects)
    print('What/Which/Who/How:\t', adj)
    print('Preposition:\t\t', preposition)
    print('===================xxxx==================')
    # print('Determiner: ', determiner)

    # millisecs = (time.time() - start_time) * 1000
    # print("--- Took %s milliseconds to analyze ---" % millisecs)
    # steps to comprehension
    # 1 - get verbs
    # 2 - find noun from the verb
    # 3 - find the tense
    # 4 - analyze the period
