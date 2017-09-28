import nltk
import sys
import time

groucho_grammar = nltk.CFG.fromstring("""
 S -> NP VP
 PP -> P NP
 NP -> Det N | Det N PP | 'I'
 VP -> V NP | VP PP
 Det -> 'an' | 'my' | 'your'
 N -> 'elephant' | 'pajamas'
 V -> 'shot'
 P -> 'in'
 """)

if len(sys.argv) > 1:
    text = sys.argv[1].split(' ')
else:
    text = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']

parser = nltk.ChartParser(groucho_grammar)

for tree in parser.parse(text):
    print(tree)
