### Here I prepare a plot of Rblast values (sequence similarity) versus shortest path length (structural distance). Sequences compared by Rblast correspond with structural motifs found by comp2ss.py, structural distance comes from clustering those motifs with forester. 


import networkx as nx
import matplotlib.pyplot as plt
import glob
import numpy as np
import math

### SET CUTOFFS

for_cutoff = 0.5 #cutoff value for Forester edge score
eval_cutoff = 0.01 #cutoff value for Rblast evalue score

### Prepare list of nodes and edges

nodeslist=[]
edgelist=[]

with open('/home/ejank/Dropbox/comp2ss/outputs/to_forester_global.csv', 'r') as spam:
	
	for line in spam:
		if line.startswith('"Source"'):
			continue
		
		source, target = line.split('\t')[0].strip('"'), line.split('\t')[1].strip('"')
		
		nodeslist.append(source)
		nodeslist.append(target)
	
		score = float(line.split('\t')[2].strip('"'))
		
		if score <= for_cutoff: #filter out edges with low scores - that is 90% of all edges...
			continue
		#if int(score)==0:
		#	continue
		edgelist.append((source, target, round(1.0/score, 2)))
	print len(edgelist)
nodes = list(set(nodeslist))
nodes = sorted(nodes, key=lambda node: int(node.split('_')[0]))
print len(nodes)

###Prepare dictionary of structures

structure_dict = {}
for item in nodes:
	key = item.split('_')[-1]
	structure_dict[key] = item

### Create graph 

G=nx.Graph()
G.add_weighted_edges_from(edgelist)
#print G.nodes()

### Filter Rblast results

out = open('/home/ejank/Dropbox/comp2ss/rblast_res/rblast_minlen20_filtered', 'w')

#for path in glob.glob("/home/ejank/Dropbox/comp2ss/rblast_res/all_nodes_unshaped_nodots_minlen20.tab"):
	#with open(path, 'r') as spam:
with open("/home/ejank/Dropbox/comp2ss/rblast_res/all_nodes_unshaped_nodots_minlen20.tab", 'r') as spamfile:
	#spamfile = open(path, 'r')
	spam = spamfile.readlines()
	for line in spam:
		if line.split('\t')[0].split('_')[0]==line.split('\t')[1].split('_')[0]: #filter out self - matches
			continue
		if line.split('\t')[1].endswith('rev'): #filter out reversed sequences
			continue
		#print line.split('\t')[10]
		
		if float(line.split('\t')[10].strip())>eval_cutoff: #filter out pairs with evalue 
			continue
		out.write('%s\t%s\t%s\n' % (line.split('\t')[0], line.split('\t')[1], line.split('\t')[10]))

	spamfile.close()
out.close()

###Create list of singletons - nodes with no edges

s = set(G.nodes())
singletons = [item for item in nodes if item not in s]
print singletons

###create file with Rblast value vs. shortest path

err_count = 0
err_names = []
plot_values = open('/home/ejank/Dropbox/comp2ss/rblast_res/plot_values_global_minlen20', 'w')

with open('/home/ejank/Dropbox/comp2ss/rblast_res/rblast_minlen20_filtered', 'r') as spam:
	for line in spam:
		#print line
		source = structure_dict[line.split('\t')[0].split('_')[1]]
		target = structure_dict[line.split('\t')[1].split('_')[1]]
		if source in singletons or target in singletons:
			str_value = 7.5
		else:
			try:
				str_value = nx.shortest_path_length(G, source, target)#nx.dijkstra_path_length(G, source, target)  #you can choose between simple length of the shortest path, or a sum of its weights. Length calculates almost instantly, values take several minutes.
			except:
				str_value = 7.5
				plot_values.write('%f\t%s\t%s\t%s\n' % (round(-math.log10(float(line.split('\t')[2].strip())), 2), str_value, line.split('\t')[0], line.split('\t')[1]))
				err_count += 1
				err_names.append((source, target))
				continue

		plot_values.write('%f\t%s\t%s\t%s\n' % (round(-math.log10(float(line.split('\t')[2].strip())), 2), str_value, line.split('\t')[0], line.split('\t')[1]))
plot_values.close()
print 'errors: ', err_names, err_count

###Make a plot

collections = {}
dataset = []

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

with open('/home/ejank/Dropbox/comp2ss/rblast_res/plot_values_global_minlen20', 'r') as spam:
	for line in spam:
		if line.split('\t')[1] in collections.keys():
			collections[line.split('\t')[1]] = collections[line.split('\t')[1]] + [float(line.split('\t')[0])]
		else:
			collections[line.split('\t')[1]] = [float(line.split('\t')[0])]
		dataset.append((line.split('\t')[0], line.split('\t')[1], line.split('\t')[2], line.split('\t')[3]))


y_val = [x[0] for x in dataset]
x_val = [x[1] for x in dataset]
#print collections

data_to_boxplot=[]

#print collections.keys()
for ind, key in enumerate(collections.keys()):
	temp = collections[key]
	
	data_to_boxplot.append(temp)

# Create a figure instance
fig = plt.figure(1, figsize=(9, 6))

# Create an axes instance
ax = fig.add_subplot(111)
ax = plt.gca()
ax.invert_yaxis()

xvals = sorted(list(set(x_val)), key=lambda xval: float(xval))
#$xticks = [frange(0, float(xvals[-2]), 0.01)] + ['singletons']
ax.set_xticklabels(xvals)
plt.xlabel('Structural distance - shortest path length')
plt.ylabel('Sequence similarity - Rblast log10(eval)')
plt.title("Forester score cutoff - %f, evalue (Rblast) cutoff - %f" % (for_cutoff, eval_cutoff))

#ax.spines['left'].set_position(('outward', 10))
#ax.spines['bottom'].set_position(('outward', 10))

#plt.xlim(0, 1000) #offset the axes
#plt.ylim(0, 1000)

# Create the boxplot
bp = ax.boxplot(data_to_boxplot)



plt.show()
plt.close()


'''
dataset = []
with open('/home/ejank/Dropbox/comp2ss/rblast_res/plot_values', 'r') as spam:
	for line in spam:
		dataset.append((line.split('\t')[0], line.split('\t')[1], line.split('\t')[2], line.split('\t')[3]))


y_val = [x[0] for x in dataset]
x_val = [x[1] for x in dataset]


plt.plot(x_val, y_val, '.')

plt.axis([0, 0.3, 0, float(max(y_val))+10])

ax = plt.gca()
ax.invert_yaxis()

plt.xlabel('Structural distance')
plt.ylabel('Sequence similarity')
plt.draw()
labels = [item.get_text() for item in ax.get_xticklabels()]
labels[5] = 'Singletons'

ax.set_xticklabels(labels)

#plt.axhline(np.mean(y_val), color='r', linestyle='dashed', linewidth=1)
#plt.savefig('/home/ejank/tetrapods/%s_gc_%s.png' % (name, region), bbox_inches='tight')
plt.show()
plt.close()


'''

