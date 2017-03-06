# forgi must be installed
# http://www.tbi.univie.ac.at/~pkerp/forgi/index.html
"""
	converts RNA sequence + secondary structure to a SHAPE-like format
	while preserving the sequence information
	author: Staszek
"""

import forgi.graph.bulge_graph as cgb
import re

class smart_sequence():
	def __init__(self, ident, seq, ss):
		#assert len(set(seq))==4
		self.ident = ident
		self.seq = seq.upper()
		self.ss = ss
		assert ss.count('(')==ss.count(')')
		self.do_shape()

	def shape_to_seq(self, range_from, range_to):
		assert range_from<=range_to
		return ''.join([i[1] for i in self.shape[range_from:range_to+1]] )	
	'''
	This part is by Ela, I'm figuring out how to make converting condensed structure back to normal. Work in progress. 
	
	def shape_start(self, range_from):
		#print 'tutaj: ', ''.join([i[1] for i in self.shape[:range_from]])
		count = len(''.join([i[1] for i in self.shape[:range_from] if i[0]!='.']))
		match = re.search('\.*', self.ss)
		
		startdots = len(match.group())
		for ind, char in enumerate(self.ss):
			if count == 0:
				match = re.search('\.*', self.ss[ind:])
				dots = len(match.group())
				return ind + dots - startdots			
			if char in ['(', ')']:
				count -= 1

		
		#return count+dots
	'''
	

	def do_shape(self):
		g = cgb.from_id_seq_struct(self.ident, self.seq, self.ss)
		
		shape = []
		#print 'tutaj: ', g.defines.keys()
		for element_id in g.defines.keys():
			#print element_id, g.get_define_seq_str(element_id)
			
			element_type = element_id[0]
			element = g.defines[element_id]
			
			element_seq = g.get_define_seq_str(element_id)
			#print 'element, seq: ', element, element_seq
			if element_type == 'h':		
				shape.append((element[0], (".", element_seq[0])))
					
			elif element_type == 'i':
				if element_seq[0]=='':
					shape.append((element[0], (".", element_seq[1])))
				else:		
					shape.append((element[0], (".", element_seq[0])))
				if len(element)==4:
					shape.append((element[2], (".", element_seq[1])))
			
			elif element_type == 's':
				shape.append((element[1], ("(", element_seq[0]) ))	
				shape.append((element[2], (")", element_seq[1])))	
			
	
			#print d, g.defines[d]
			
		self.shape = [i[1] for i in sorted(shape, key=lambda x:x[0])]
		self.shapess = ''.join([i[0] for i in self.shape])
		
		
if __name__ == "__main__":
	
	ss= '.................((.........(((...((((.....((((((.((((....((((.........((((........(((((......((((((..........((.(((((..((((.....((((((((.....................................................(((............................................)))............................((((((....((.((.((((.((((..((((.......))))))))..)))).)).))..)))))).................................................................................................................))))))))...........................((((((.....)))))).......................................................(((((((.((((.....)))).)))))))...((((((..((((((((..........((((.(((.....))).)))).........)))))))).......))))))...............................................((((((((................)))))))).((((((((((...........................................))))))))))..)))).)))))))..........))))))......)))))..........))))......))))....)))).)))))).))))....)))..................(((((((..................................(((((.(((......(((((..((((...........................................(((...)))(((((((.(((((((.......................................)))))))..))))))).))))..)))))......))).)))))............((((....))))....................)))))))...............))........'	
	seq='AAGAGGAAGAUAGGUAACCUAUUAAAAUGUCAGCGGCUGUUACGUUUGCUUACCAGUAUUUUUUUUUUUUAGUUUCUUUUUUUUGUACAUUUUCCAUUUGAGUUUUCUAUCGUGUAAGCCUCAGAGAUUUGGUAGACGCUUAAUGGUGGAAAGGUUGGGUUGGAUUUAGGAUUGAGAUCUCAAGUUAGCAGGCAGUUAUAAAUUUUUUUUUUUACGAAGAAAUAUGAGUGCGCUGGUGCCAGUAUAGAUGCUUAUGUAUACGUGUAUUUGUGGUUUUUGCUAUUCUUCUACUUAUAGAUGGCUAAAAUCUGAGUUUGAAGGAUUGCGAACCAUAAAUACUUGAAAAUUACUAUUGCAUUUAGUUGCUAGAGUACAUUUUUUCAACAAUUAUUCCUUCUUUAGUACCAAUUCUGUUUUCGUCUUAACCUCUUCAUUAUUAUGGAAAAUGUCUACCAUUACCACACCCACACACAAAUAUUACGGCUAAUUGUUUAUUAGCUAAAUUUCCAUGAGCACACUUUUUAUUUUUUUCUCGUUUUCUUAUACCUAGUAUAUUUUCUGUCACUUUUAAAGUGACAGAAAAAAAGGAGUUUGAAUUAGACUUGCAAAACGGACAGUAUUAAUAAUACUGUCACUCUUAAUGUCUAAUUUAUCGUCAACUCUGUAAAAAGAAAACAAGAAAAAGAAAAUUGGUGGAUAAAAGUAUAUAUAGAAAUGGUUUAUUCUAGUUUUUUCCAUUUCUCAGUAGAUUUUUGCCUUUUAAGAGAAUAAAUUCAACUAAAAAAAGGUUAAAAGAAAAAUCUAUUCACUGAACUUACCGAUAGAAAUUUCAAAUGUGUCAAGUACAUUAAAAAAGGAAACAGAGGAAAAAAAAAGGUAGGCAAACAAGCCAAAAGACAAGGACACCCUUCCUCAAGCACCGAAUAGGUUUGCGAGCGAAUAGUAACCGAAAAAUGAUACAAGACGAAAAAACAUAAUUUGAGAUUUUUCAAGAUGGAUUUUUUUAGAUAUCUAUUUAAACAAUUUUGAUGAUCAAUACAGUAUUUUUGUCGCAUCCUUGUUAAAGUAAGGACGGACAUUAAUUUCCAAACGGAAAGAACUGUGUGUUCAUUUUAUGGAUUUUCGUGUUGUACAUUUUUUUCAGCUGCGUUAGCAGUUACUUUUUCCACAAUACUUUCGGUGCAUACAGAUAAUUUUUGGAAACAUUU'
	print ss
	print seq
	#print len(ss), len(seq)
	xyz = smart_sequence('test', seq, ss)
	#print xyz.ss
	#print xyz.seq
	print 'shape ', xyz.shape
	print 'shapess ', xyz.shapess
	print 'shape to seq', xyz.shape_to_seq(0, 25)
	
	#start = xyz.shape_start(0)
	#stop = start + len(xyz.shape_to_seq(0, 34))
	
	#print start
	#print ss[start : stop]

