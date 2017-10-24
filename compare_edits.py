# CompareStringEdits function
# ---------------------------
# For comparing two sentence or document strings based on word-level edits, using the difflib package's Differ method,
# adding functionality to track sequences of words in common and sequences of words that were inserted (+) or deleted (-).
# May be used to construct similarity scores beyond just the number of words two docs have in common, such as the
# likelihood that they represent versions of the same original text, based on the average length of common sequences,
# percentage of the text that falls into common sequences, or totaly number of inserted or deleted segments.

from difflib import Differ
from statistics import mean

def GetStringEdits(a, b):
	alines = a.replace(' ', '\n').splitlines(1)
	blines = b.replace(' ', '\n').splitlines(1)
	d = Differ()
	edits = list(d.compare(alines, blines))
	edittypes = [' ', '-', '+']
	curredits = [[] for t in edittypes]
	alledits = []
	for d in range(len(edits)):
		t = edittypes.index(edits[d][0])
		if len(curredits[t])>2 and curredits[t][2]:
			curredits[t][2] += edits[d][2:].replace('\n', ' ')
		else:
			if curredits[(t+1)%3]:
				alledits.append(curredits[(t+1)%3])
				curredits[(t+1)%3] = []
			elif curredits[(t+2)%3]:
				alledits.append(curredits[(t+2)%3])
				curredits[(t+2)%3] = []
			curredits[t] = [d, edittypes[t], edits[d][2:].replace('\n', ' ')]
	for t in range(len(curredits)):
		if curredits[t]: alledits.append(curredits[t])
	return alledits

# Example Use
a = 'insert the original text'
b = 'insert a revised version of the text'
edits = GetStringEdits(a, b)
for start,change,text in edits:
	print('positions %.2d - %.2d: %s %s' % (start, start + len(text), change, text))

# Prints Out:
'''
positions 00 - 07:   insert 
positions 01 - 22: + a revised version of 
positions 05 - 09:   the 
positions 06 - 15: - original 
positions 07 - 11:   text
'''


def MatchingSegmentStats(a, b):
	edits = GetStringEdits(a, b)
	match_lengths = [len(text) for start,change,text in edits if change==' ']
	if len(match_lengths) == 0: return 0
	return {'max_match_len':max(match_lengths),
			'avg_match_len':mean(match_lengths),
			'tot_match_len':sum(match_lengths),
			'num_edits':len(edits) - len(match_lengths),
			'pct_matching':100*sum(match_lengths) / mean([len(a),len(b)])}

# Example Use
a = 'insert version 1 of the same text'
b = 'insert version 2 of the same text'
c = 'insert something totally unrelated'
d = 'insert another version of the first text'
for x,y in [(a,b),(a,c),(a,d)]:
	matchstats = MatchingSegmentStats(x, y)
	print('text1: \"%s...\", text2: \"%s...\"' % (x[:20], y[:20]))
	print(' -- max length of matching segment:     %2d chars' % matchstats['max_match_len'])
	print(' -- avg length of matching segment:     %2d chars' % matchstats['avg_match_len'])
	print(' -- sum lengths of matching segments:   %2d chars' % matchstats['tot_match_len'])
	print(' -- num edits (non-matching segments):  %2d edits' % matchstats['num_edits'])
	print(' -- pct doc in matching segments:       %.2f%% of doc\n' % matchstats['pct_matching'])

# Prints Out:
'''
text1: "insert version 1 of ...", text2: "insert version 2 of ..."
 -- max length of matching segment:     16 chars
 -- avg length of matching segment:     15 chars
 -- sum lengths of matching segments:   31 chars
 -- num edits (non-matching segments):   2 edits
 -- pct doc in matching segments:       93.94%% of doc

text1: "insert version 1 of ...", text2: "insert something tot..."
 -- max length of matching segment:      7 chars
 -- avg length of matching segment:      7 chars
 -- sum lengths of matching segments:    7 chars
 -- num edits (non-matching segments):   2 edits
 -- pct doc in matching segments:       20.90%% of doc

text1: "insert version 1 of ...", text2: "insert another versi..."
 -- max length of matching segment:      8 chars
 -- avg length of matching segment:      6 chars
 -- sum lengths of matching segments:   26 chars
 -- num edits (non-matching segments):   4 edits
 -- pct doc in matching segments:       71.23%% of doc

'''


