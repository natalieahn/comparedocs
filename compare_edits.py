# CompareStringEdits function
# ---------------------------
# For comparing two sentence or document strings based on word-level edits, using the difflib package's Differ method,
# adding functionality to track sequences of words in common and sequences of words that were inserted (+) or deleted (-).
# May be used to construct similarity scores beyond just the number of words two docs have in common, such as the
# likelihood that they represent versions of the same original text, based on the average length of common sequences,
# percentage of the text that falls into common sequences, or totaly number of inserted or deleted segments.

from difflib import Differ

def CompareStringEdits(a, b):
	alines = a.replace(' ', '\n').splitlines(1)
	blines = b.replace(' ', '\n').splitlines(1)
	d = Differ()
	difs = list(d.compare(alines, blines))
	diftypes = [' ', '-', '+']
	currdifs = [[] for t in diftypes]
	alldifs = []
	for d in range(len(difs)):
		t = diftypes.index(difs[d][0])
		if len(currdifs[t])>2 and currdifs[t][2]: currdifs[t][2] += difs[d][2:].replace('\n', ' ')
		else:
			if currdifs[(t+1)%3]:
				alldifs.append(currdifs[(t+1)%3])
				currdifs[(t+1)%3] = []
			elif currdifs[(t+2)%3]:
				alldifs.append(currdifs[(t+2)%3])
				currdifs[(t+2)%3] = []
			currdifs[t] = [d, diftypes[t], difs[d][2:].replace('\n', ' ')]
	for t in range(len(currdifs)):
		if currdifs[t]: alldifs.append(currdifs[t])
	return alldifs

# Example Use
a = 'insert the original text'
b = 'insert a revised version of the text'
difs = CompareStringEdits(a, b)
for dif in difs:
	print('positions %d - %d: %s %s' % (dif[0], dif[0] + len(dif[1]), dif[1], dif[2]))

# Prints Out:
'''
positions 0 - 1:   insert 
positions 1 - 2: + a revised version of 
positions 5 - 6:   the 
positions 6 - 7: - original 
positions 7 - 8:   text
'''
