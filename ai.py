#!/usr/bin/python

import nltk
from sys import stdin
import re

#from nltk.corpus import stopwords
#stopwords = stopwords.words('english')
#stopwords.remove('i')

#
# This tokeniser understands difference between period . and decimal point
from nltk.tokenize.punkt import PunktWordTokenizer


class Session:
	def __init__(self):
		self.pattern = re.compile('\s+')
		self.lines = []

	def read_input(self):
		print "Enter your statements(s) and then question(s). Terminate by pressing (Control + D) :"
		for line in stdin.readlines():
			self.lines.append( ((self.pattern.sub(' ',line)).strip()) )
			#self.lines.append(line)
		#print self.lines
		return self.lines

class NLTK:
	def __init__(self,lines):
		self.lines=lines
		print self.lines
		for line in self.lines:
			PunktWordTokenizer().tokenize(line)
		self.tokens= []
		self.word_tag_pairs = []
		self.tokens = [ [token for token in PunktWordTokenizer().tokenize(line) ] for line in self.lines ]
		print self.tokens
		self.word_tag_pairs = [ [wtp for wtp in nltk.pos_tag(token)] for token in self.tokens ]
		print self.word_tag_pairs
		self.romanSearch = re.compile(r'.*\b([IVXCLM])(\s+|$)$')
		self.stgrammar = r"""
			NP:	{<[ABCDGIJNPSTUV].*>}
				{<NN>?}
				{<NNP>?}
			VP:	{<VBZ>}
			NP:	{(<CD><NNS>)|(<PRP|NN[PS]>)}
			"""
		self.stcp = nltk.RegexpParser(self.stgrammar)
		self.d = {}
		self.d.update({"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000})
	
	def check_if_Question_or_Statement(self,line):
		return  next ((bool(1)  for (a, b) in line if b == 'WRB' ),bool(0))

	def validateRoman(self,line):
		hasRomanNumeral = self.romanSearch.search(line)
		if hasRomanNumeral == None:
			print(
			"""Not a valid roman numeral from [IVXCLM]. Try again. Statement should be of the form:
			[word_in_your_language] is [ROMAN_NUMERAL_IN_UPPERCASE]
			For Eg:
			chuck is X
			duck means V
			""")

	def tree2dict(self,line):
		tree = self.stcp.parse(line)
		print tree
		terms = get_terms(tree)		
		return terms

	def train(self,terms):
		for term in terms:
			for word,tag in term:
				print word,tag
			print
		#for subtree in trees.subtrees():
		#	if subtree.node == 'NP':
		#		self.do_something_with_subtree(subtree)
		#	else:
		#		self.do_something_with_leaf(subtree)
		#	for subtree in trees.subtrees(filter=lambda t: t.node == 'NP'):
    			# print the noun phrase as a list of part-of-speech tagged words
    				
	def validateQuestion(self):
		print self.lines


def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.node =='NP' or t.node == "VP"):
        yield subtree.leaves()

def get_terms(tree):
    for leaf in leaves(tree):
        #term = [ (w,t) for w,t in leaf if acceptable_word(w) ]
        term = [ (w,t) for w,t in leaf ]
        yield term

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(word.lower() not in stopwords)
    return accepted

if __name__ == '__main__':
	s = Session()
	firstrun=bool(1)
	lines = s.read_input()
    	n = NLTK(lines)
	for line in n.word_tag_pairs:
		question = n.check_if_Question_or_Statement(line)
		if(question and firstrun):
			sys.exit("""
			Dude, I have not idea what you are talking about. Kindly train me with statements like :
			dhishum means  V
			pichik is X
			""")
		elif (not question):
			# logic to handle validating and entering the data in out dictinary
			terms = n.tree2dict(line);
			n.train(terms);
			firstrun=bool(0)
		elif (question and not firstrun):
			#logic to handle validating and answering the question
			n.validateQuestion(line)
