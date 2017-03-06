import itertools

#The first part of the script generates a file containing all types of structural motifs found by comp2ss to be compared by forester.
#That is - clustering of clusters. Metaclustering, yeah.



ss=[]
with open('/home/ejank/Dropbox/comp2ss/outputs/rfam_5_12.csv', 'r') as eggs:
	for line in eggs:
		if not line.startswith('"R'):
			continue
		#if line=='\n':
		#	print 'tu'
		#	continue
		
		
		ss.append(line.strip().split('\t')[3].strip('"'))


to_forester = list(set(ss))
to_forester = [(ind, el) for ind, el in enumerate(to_forester)]
#print to_forester

combinations = list(itertools.combinations(to_forester, 2))
out = open('/home/ejank/Dropbox/comp2ss/outputs/to_forester', 'w')
for pair in combinations:
	out.write("%s_%s\t%s\n" % (pair[0][0], pair[0][1], pair[0][1]))
	out.write("%s_%s\t%s\n" % (pair[1][0], pair[1][1], pair[1][1]))



#This part is to make a .csv file for visualisation in Gephi. 

'''
csv = open('/home/ejank/Dropbox/comp2ss/outputs/to_forester_global.csv', 'w')
csv.write('"Source"\t"Target"\t"Weight"\t"Type"\n')


with open('/home/ejank/Dropbox/comp2ss/outputs/to_forester.res', 'r') as spam:
	for line in spam:
		csv.write('"%s"\t"%s"\t"%s"\t"%s"\t"Undirected"\n' % (line.split('\t')[0], line.split('\t')[1], line.strip().split('\t')[6], line.split('\t')[5]))


#use this for global comparison with relative score	
	
#with open('/home/ejank/Dropbox/comp2ss/outputs/to_forester_global.res', 'r') as spam:
#	for line in spam:
#		csv.write('"%s"\t"%s"\t"%s"\t"Undirected"\n' % (line.split('\t')[0], line.split('\t')[1], line.strip().split('\t')[-1]))

'''		
