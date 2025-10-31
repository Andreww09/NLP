import nltk
from nltk import Production, CFG
from nltk.tokenize import word_tokenize
import svgling
import spacy


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('universal_tagset')

sentences = [
    "Flying planes can be dangerous",
    "The parents of the bride and the groom were flying",
    "The groom loves dangerous planes more than the bride"
]

all_sentences = nltk.CFG.fromstring("""
S -> NP VP NP | NP VP
VP -> V | V A | V VP 
NP -> Det NP | NP PP NP | A NP | N
A -> 'dangerous' | 'flying'
V -> 'loves' | 'can' | 'be' | 'were' 
N -> 'groom' | 'planes' | 'bride' | 'parents'
PP -> P | P PP
P -> 'more' | 'than' | 'and' | 'of'
Det -> 'the'
""")

_third_sentence = nltk.CFG.fromstring("""
S -> NP VP NP
VP -> V
NP -> Det NP | NP P NP | A NP | N
A -> 'dangerous'
V -> 'loves' 
N -> 'groom' | 'planes' | 'bride'
P -> 'more than'
Det -> 'the'
""")

_second_sentence = nltk.CFG.fromstring("""
S -> NP VP
VP -> V A
NP -> Det NP | NP P NP | N
A -> 'flying'
V -> 'were' 
N -> 'parents' | 'bride' | 'groom'
P -> 'of' | 'and'
Det -> 'the'
""")

_first_sentence = nltk.CFG.fromstring("""
S -> NP VPP
VPP -> V | VP | V VP
VP -> V A
NP -> A N 
A -> 'flying' | 'dangerous'
V -> 'can' | 'be' 
N -> 'planes' 
""")

# ex 2
cparser = nltk.ChartParser(all_sentences)
for sentence in sentences:
    for tree in cparser.parse(sentence.lower().split()):
        print(tree)
        svgling.draw_tree(tree)



# ex 3
nlp = spacy.load("en_core_web_sm")

def parse_sentence(sentence):
    doc = nlp(sentence)
    for token in doc:
        print(f"{token.text} {token.dep_} {token.head.text}")

for sentence in sentences:
    parse_sentence(sentence)