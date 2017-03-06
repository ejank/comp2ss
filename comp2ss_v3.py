#import difflib
import re
import sys, subprocess
import shapes
import os
import tempfile
import forgi.graph.bulge_graph as cgb


#This script is supposed to compare a pair of structures (stored as structure objects) and return all common, valid structural motifs, including information about repeating motifs

class structure:
	def __init__(self, name, structure, length):	#, sequence):
		self.name = name
		self.structure = structure
		self.length = length
		#self.sequence = sequence
		self.matches=[]
		self.patterns={}

	def create_matches(self, str2):
		blocks = paired_common_substrings(self.structure, str2.structure) #find common paired substrings. 
		
		#print blocks
		#patterns = []
		used1 = []
		used2 = []
		for s1, s2, st in blocks:
			starts1list, starts2list = [], []
			
			for s in s1:
				#if bool(set(used1)&set(range(s,s+len(st)))): #this is to prevent defining overlapping substrings as separate matches
				#	continue
				starts1list.append(s)
				used1.extend(range(s,s+len(st)))
			for e in s2:
				#if bool(set(used2)&set(range(e,e+len(st)))): #this is to prevent defining overlapping substrings as separate matches
				#	continue
				starts2list.append(e)
				used2.extend(range(e,e+len(st)))
			
			#print starts1list
			#print starts2list
			
			if starts1list==[] or starts2list==[]: #drop this motif if it doesn't have a start index in either string
				continue
			
			'''
			if (st in self.patterns and st in str2.patterns):
				m=match('%s_%i' % (self.name, self.patterns.index(st)), starts1list, '%s_%i' % (str2.name, str2.patterns.index(st)), starts2list, len(st), st) #create matches for all motifs
			elif (st in self.patterns and st not in str2.patterns):
				str2.patterns.append(st)
				m=match('%s_%i' % (self.name, self.patterns.index(st)), starts1list, '%s_%i' % (str2.name, str2.patterns.index(st)), starts2list, len(st), st) #create matches for all motifs
			elif (st not in self.patterns and st in str2.patterns):
				self.patterns.append(st)
				m=match('%s_%i' % (self.name, self.patterns.index(st)), starts1list, '%s_%i' % (str2.name, str2.patterns.index(st)), starts2list, len(st), st) #create matches for all motifs
			else:
				self.patterns.append(st)
				str2.patterns.append(st)
				m=match('%s_%i' % (self.name, self.patterns.index(st)), starts1list, '%s_%i' % (str2.name, str2.patterns.index(st)), starts2list, len(st), st) #create matches for all motifs
			'''
			my_nodes=[]
			part_nodes=[]			



			if st not in self.patterns.keys():
				self.patterns[st] = starts1list
			if st not in str2.patterns.keys():
				str2.patterns[st] = starts2list

			



			m=match(self.name, starts1list, str2.name, starts2list, len(st), st) #create matches for all motifs

			self.matches.append(m)	
			str2.matches.append(m)	
	
		return self.matches

			
	def print_matches(self):
		a=[]
		for item in self.matches:
			a.append(item.ID())

		return a
		
	def split_matches(self):
		for item in patterns:
			pass


class match(structure): #I'd like to be able to easily come back to true structure from Shape, though I don't know yet how to do that
	def __init__(self, me, me_startlist, partner, partner_startlist, length, structure):
		self.me = me
		self.mestart = me_startlist
		self.partner = partner
		self.partnerstart = partner_startlist
		self.length = length
		self.structure = structure
		
	def ID(self):
		return (self.me, self.mestart, self.partner, self.partnerstart, self.structure)



def overlap(x,y):
	return max(0,min(x[-1], y[-1]) - max(x[0], y[0]) + 1)


def count_brackets(string):
	opens = string.count('(')
	ends = string.count(')')
	return opens-ends


def ensure_pairs(string): #checks if matching substring is a valid structural motive. This function works good when we compare SHAPE structures, which are less comlicated than "raw" structures. 
#ensure_pairs_v3() is good for working with raw structures
#this function looks terrible, would be nice to rewrite it in a more concise way if it exists
	right, left = 0, 0
	if len(string)<2:
		return
	while string[0]==')' or string[0] == '.': #remove dots and closing brackets from the beginning
		string=string[1:]
		left+=1
		if len(string)<2:
			return
	while string[-1]=='(' or string[-1] == '.': #remove dots and opening brackets from the end
		string=string[:-1]
		right+=1
		if len(string)<2:
			return
	i = count_brackets(string)
	if i == 0: #opens == ends
		print 'out: ', left, right, string
		return left, right, string #below: checking if brackets are paired
	while i<0: #more ends than opens
		if string[-1]==')':
			i=i+1
		string=string[:-1]
		right+=1
	while i>0: #more opens than ends
		if string[0]=='(':
			i=i-1
		string=string[1:]
		left+=1
	while string[0]==')' or string[0] == '.':
		string=string[1:]
		left+=1
	while string[-1]=='(' or string[-1] == '.':
		string=string[:-1]
		right+=1
	out = [(left, right, string)]
	print 'out: ', out
	return out


###NEW PART


def ensure_motif_is_valid(string): #checks if matching substring is a valid structural motive
#this function looks terrible, would be nice to rewrite it in a more concise way if it exists
	right, left = 0, 0
	i = count_brackets(string)
	if i == 0: #opens == ends
		try:
			g = cgb.from_id_seq_struct('test', 'a'*len(string), string)
			
		except:
			return [0]
		
		return left, right, string #below: checking if brackets are paired
	while i<0: #more ends than opens
		if string[-1]==')':
			i=i+1
		string=string[:-1]
		right+=1
	while i>0: #more opens than ends
		if string[0]=='(':
			i=i-1
		string=string[1:]
		left+=1
	while string[0]==')' or string[0] == '.':
		string=string[1:]
		left+=1
	while string[-1]=='(' or string[-1] == '.':
		string=string[:-1]
		right+=1
	try:
		g = cgb.from_id_seq_struct('test', 'a'*len(string), string)
			
	except:
		return [0]
		
	return left, right, string

def remove_trailing_dots(string):#removes trailing dots and unclosed brackets from both ends of a string

	right, left = 0, 0
	if len(string)<2:
		return
	while string[0]==')' or string[0] == '.': #remove dots and closing brackets from the beginning
		string=string[1:]
		left+=1
		if len(string)<2:
			return
	while string[-1]=='(' or string[-1] == '.': #remove dots and opening brackets from the end
		string=string[:-1]
		right+=1
		if len(string)<2:
			return
	
	out = [left, right, string]
	
	return out #below: checking if brackets are paired



def ensure_pairs_v3(string): #checks if given string is a valid structural motive, if not, returns substrings that ARE valid motives
#this function (these functions, ha) look super - terrible, but they seem to be working
	
	a = remove_trailing_dots(string)
	if a == None:
		return
	string = a[2]
	left = a[0] 
	right = a[1]

	
	
	i = count_brackets(string)
	if i == 0:
		if ensure_motif_is_valid(string)!=[0]:
			return [(left, right, string)]
			
	
	match = re.finditer('\(+[\.*\(*]*\.*[\)*\.*]*\)+\.*', string) #find all patterns consisting of brackets and dots 
	
	validated_motifs=[]
	while True:
		try:		
			a=match.next()
			b = ensure_motif_is_valid(a.group()) #validate motifs - make sure all brackets are paired
			if len(b) == 1:
				break
			validated_motifs.append([a.span()[0]+left+b[0], a.span()[1]+left-b[1], b[2]]) #saved like this: (left index, right index, structure)
			
		except StopIteration:
			break
		
	if not match:
		return
	
	check=[]
	if validated_motifs==[]:
		return
	
	# This part checks if found motifs are adjacent, and if yes, concatenates them
	structure=validated_motifs[0][2]
	bg_index=validated_motifs[0][0]
	end_index=validated_motifs[0][1]

	if len(validated_motifs)==1:
		check.append((bg_index, end_index, structure))

	for ind, el in enumerate(validated_motifs[1:]):
		
		if el[0] == end_index: #if start index of element n is equal to end index of element n-1, we have a match!
			structure=structure+el[2]
			end_index = el[1]
			
		else:
			x=remove_trailing_dots(structure) #remove trailing dots again
			check.append((bg_index+x[0], end_index-x[1], x[2]))
			bg_index=el[0]
			end_index=el[1]
			structure=el[2]

		if ind == len(validated_motifs[1:])-1:
			x=remove_trailing_dots(structure)
			check.append((bg_index+x[0], end_index-x[1], x[2])) # saved like this: (left index, right index, structure)
	
	return check
			 



###/NEW PART

def paired_common_substrings(s1, s2):  #based on a Longest Common Substring algorithm implementation from http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python
	m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))] 
	for x in xrange(1, 1 + len(s1)): #here a matrix of similarities is constructed
		for y in xrange(1, 1 + len(s2)):
			if s1[x - 1] == s2[y - 1]:
				m[x][y] = m[x - 1][y - 1] + 1
				
			else:
				m[x][y] = 0
	#print(m)
	used=[]
	strings=[]
	for i in reversed(range(0, len(s1)+1)):
		for j, el in enumerate(m[i]):
			
			if (i, j) in used:
				continue
			if el==0 or el==1:
				continue
			string = (i-el, j-el, s2[j-el:j]) #here all found substrings longer than 1 are saved. (start index in s1, start ind in s2, structure)
			strings.append(string)
			used.append((i, j))
			for n in range(1, el): #this is to prevent saving substrings of an already saved string (example: ((..)) and ((..) and ((.. and so on)
				used.append((i-n, j-n))	
	
	out=[]
	
	for s1, s2, el in strings:
		#print s1, s2, el
		el = ensure_pairs_v3(el) #get rid of all common substrings that are not a valid structural motif
		
		if el== None:
			continue
		if type(el)==list:
			for motif in el:
				out.append((s1+motif[0], s2+motif[0], motif[2])) #correct indices for any characters sliced off by ensure_pairs()
		else:#elif type(el)==tuple:
			out.append((s1+el[0], s2+el[0], el[2])) #correct indices for any characters sliced off by ensure_pairs()
	
	template=list(set([el[2] for el in out])) #list of all structural motifs found
	
	res=[]
	for element in template: #this part is to format the output
		starts1, starts2 = [], []
		for i1, i2, el in out:
			if element==el:
				starts1.append(i1)
				starts2.append(i2)
		element=(list(set(starts1)), list(set(starts2)), element) #element has following info: list of start indices in s1, list of start indices in s2, structure
		res.append(element)						#there is only one element for each structural motif
	res.sort(key=lambda x: len(x[2]), reverse=True) #results are sorted from longest structural element to the shortest.
	return res
	

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def runcomp(input_folder, output_folder, nodes_folder, filename):
	
	csv = open('%stemp.csv' % output_folder, 'a')
	f= open('%s%s' % (input_folder, filename), 'r')
	l1=f.readline()
	i=1
	rfam1, ss1 = l1.split('\t')[0], l1.split('\t')[1]	#rfam1, ss1, seq1 = l1.split('\t')[0], l1.split('\t')[1], l1.split('\t')[-1]
	structure1 = structure(rfam1, ss1, len(ss1))		#, seq1)
	a = file_len('%s%s' % (input_folder, filename))
	
	while l1:
		
		l2=f.readline()
		i+=1
		if len(l2.split('\t')) != 3:
			break

		rfam2, ss2 = l2.split('\t')[0], l2.split('\t')[1]	#rfam2, ss2, seq2 = l2.split('\t')[0], l2.split('\t')[1], l2.split('\t')[-1]

		if rfam1==rfam2:
			continue
		
		structure2 = structure(rfam2, ss2, len(ss2))		#, seq2)
		structure1.create_matches(structure2)
		if l1.split('\t')[0] != rfam1:
			
			out = open('%s%s_out' % (nodes_folder, rfam1), 'a')
			for item in structure1.matches[:-1]:
				
				csv.write('"%s_%s"\t"%s_%s"\t"1"\t"%s"\t"Undirected"\n' % (item.me, item.structure, item.partner, item.structure, item.structure))
				out.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (item.me, item.mestart, item.partner, item.partnerstart, item.length, item.structure))
			rfam1, ss1 = l1.split('\t')[0], l1.split('\t')[1]	#rfam1, ss1, seq1 = l1.split('\t')[0], l1.split('\t')[1], l1.split('\t')[-1]
			structure1 = structure(rfam1, ss1, len(ss1))		#, seq1)
			structure1.create_matches(structure2)
			
			out.close()
			
		#print i, a
		if i==a:
			
			out = open('%s%s_out' % (nodes_folder, rfam1), 'a')
			for item in structure1.matches:
				
				csv.write('"%s_%s"\t"%s_%s"\t"1"\t"%s"\t"Undirected"\n' % (item.me, item.structure, item.partner, item.structure, item.structure))
				out.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (item.me, item.mestart, item.partner, item.partnerstart, item.length, item.structure))
			out.close()
		
		l1=f.readline()
		i+=1



'''
############### DO THE JOB ###############



input_folder = '/home/ejank/Dropbox/comp2ss/inputs/'
output_folder = '/home/ejank/Dropbox/comp2ss/outputs/'
nodes_folder = '/home/ejank/Dropbox/comp2ss/nodes/'


filelist = os.listdir(input_folder)
for filename in sorted(filelist): 
	if filename.split('.')[-1]=='txt':	
		print filename
		runcomp(input_folder, output_folder, nodes_folder, filename)


eggs=open('%srfam_5_12.csv' % output_folder, 'w')
eggs.write('"Source"\t"Target"\t"Weight"\t"Label"\t"Type"\n')

csv = open('%stemp.csv' % output_folder, 'r')

a=set(csv.readlines())

for line in a:
	eggs.write(line)	

os.remove('%stemp.csv' % output_folder)

'''

####################
a=('RF00773', '(.(.((.((.()).)).).).)')
shape_a=('RF00773', '(.(.(((.(.)).).).).)')

b=('RF01663', '(.(.(.(.(.()).).).).)(.(.((.()).).).)')
c=('RF00553', '(.((.(.((((.((.().).).).).).).).).))(()(().))')
d=('RF00794', '(.(.(.()).).)')
e=('RF01050', '((.(.(.(.(.(.(.(.(.(.((()(.(.(.(.(.()).).).).))()(.().)(.(.(.().).).)()()).).).).).).).).).).)((.(.(.(()(.().)).).).)()))')
shape_e=('RF01050', '((.(.(.(.(.(.(.(.(.(.(((.)(.(.(.(.(.(.)).).).).))(.)(.(.).)(.(.(.(.).).).)(.)(.)).)).).).).).).).).)((.(.(.((.)(.(.).)).).).)(.)))')
f=('ala', '..(((...)))()...().((...))..()')
g=('kot', '...((.)).().().(((...)))()')
h=('RF00231', '(.(.().).)(.(.(.().).).)(.((.()).).)(.().)')
i=('RF00191', '(.(.(.()).).)(.(.(.(.(.())))).)')
j=('RF01242', '((.((.()).).)((.()).))((.(.().).).)')
k=('RF00458', '(.().)()(.(.().).)(.().)')
    

query1 = shape_a #HERE change values to point at structures
query2 = shape_e
query3 = a

structure1 = structure(query1[0], query1[1], len(query1[1]))
structure2 = structure(query2[0], query2[1], len(query2[1]))
#structure3 = structure(query3[0], query3[1], len(query3[1]))

structure1.create_matches(structure2)
#structure1.create_matches(structure3)

print structure1.name, structure1.structure, ' and ', structure2.name, structure2.structure

for item in structure1.print_matches():
	print item 
#print structure2.name, structure2.structure, ' and ', structure1.name, structure1.structure
#structure2.print_matches()
print
print structure1.patterns

###################
'''
if __name__ == '__main__':
	print sys.argv[1]
	
	runcomp(sys.argv[1])

'''

### Do puszczania na lokalnym komputerze z folderu w ktorym sa pliki wsadowe:
# for x in *.txt; do python /home/ejank/rfam_git/rfam_shapes/test.py $x; done

