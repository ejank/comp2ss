###Generate inputs for comp2ss.py
###Input - a file with all rfam families: rfamid, ss, seq - generqated using make_clean_seq.py


import itertools
import shapes


def chunks(l, n):
    """ Yield successive n-sized chunks from l - a list.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

lista=[]

with open("/home/ejank/Dropbox/comp2ss/outputs/rfamv12_clean_ss_seq.txt", "r") as database: # a database of Rfam structures and sequences

	for line in database:
		rfam, ss, seq = line.split('\t')[0], line.split('\t')[1], line.split('\t')[2] 
		#print rfam, ss, seq
		try:
			entry = shapes.smart_sequence(rfam, seq, ss) #reduce structure to shape
			if entry.shapess == '':
				continue
			lista.append([rfam, entry.shapess, seq])
		except:
			print 'error'
#print lista

combinations = list(itertools.combinations(lista, 2))
	
for chunkid, chunk in enumerate(chunks(combinations, 1000)):
	fname = "comp_%s.txt" % chunkid
	f = open('/home/ejank/Dropbox/comp2ss/inputs/%s' % fname, 'w')
	#print chunk
	for pair in chunk:
		#print pair
		if pair[0][0] == pair[1][0]:
			print pair
			continue		
		
	
		print >>f, "%s\t%s\t%s" % (pair[0][0], pair[0][1], pair[0][2].strip()) #name, structure (shaped), sequence
		print >>f, "%s\t%s\t%s" % (pair[1][0], pair[1][1], pair[1][2].strip())
	f.close()

