from textblob import TextBlob
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
    verbs = []
    for tag in tags:
        if 'VB' in tag[1] or 'RP' in tag[1]:
            verbs.append(tag)
    return verbs

def get_determiner(verbs, all_tags):
    if len(verbs) > 0:
        verb = verbs[len(verbs) - 1]
        index = all_tags.index(verb)
        tags = all_tags[index+1:]
        nouns = []
        for tag in tags:
            if 'DT' in tag[1]:
                return tag

def noun_before_verbs(verbs, all_tags):
    if len(verbs) > 0:
        verb = verbs[0]
        index = converted_tags.index(verb)
        tags = all_tags[:index]

        nouns = []
        for tag in tags:
            if 'NN' in tag[1] or 'PRP' in tag[1] or 'EX' in tag[1] or 'CC' in tag[1]:
                nouns.append(tag)
        return nouns

def noun_after_verb(verbs, all_tags):
    if len(verbs) > 0:
        verb = verbs[len(verbs) - 1]
        index = all_tags.index(verb)
        tags = all_tags[index+1:]
        first_index = get_first_index_of('NN',tags)
        tags = tags[first_index:]
        # return tags
        nouns = []
        for tag in tags:
            if 'NN' in tag[1] or 'IN' in tag[1]:
                nouns.append(tag)
        return nouns

def adj_after_verb(verbs, all_tags):
    if len(verbs) > 0:
        verb = verbs[len(verbs) - 1]
        index = all_tags.index(verb)
        tags = all_tags[index+1:]
        # return tags
        adjs = []
        for tag in tags:
            if 'JJ' in tag[1]:
                adjs.append(tag)
        return adjs


text = '''
Menan Vadivel was born in Sri Lanka.
'''
text1 = '''
Menan Vadivel's birth place is Sri Lanka.
'''
text2 = '''
Herman Goring is a doctor
'''

text3 = '''
A tuple is a sequence of immutable Python objects.
'''

text4 = '''
The girl is learning how to drive
'''

text5 = '''
Hitler was arrested and tried for high treason
'''

text6 = '''
Rob can use Bob on his farm.
'''

if len(sys.argv) > 1:
    text = sys.argv[1]

converted_tags = compound(text)
verbs = get_verbs(converted_tags)
subjects = noun_before_verbs(verbs, converted_tags)
objects = noun_after_verb(verbs, converted_tags)
determiner = get_determiner(verbs, converted_tags)
adj = adj_after_verb(verbs, converted_tags)

print('Tags: ', converted_tags)
print('Subjects: ', subjects)
print('Verb is: ', verbs)
print('Which/how: ', adj)
print('Object: ', objects)
print('Determiner: ', determiner)

millisecs = (time.time() - start_time) * 1000
print("--- Took %s milliseconds to analyze ---" % millisecs)
# steps to comprehension
# 1 - get verbs
# 2 - find noun from the verb
# 3 - find the tense
# 4 - analyze the period
