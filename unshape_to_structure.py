### Script for unshaping - extracting structures from shape condensed structures. Based on shapes.py and unshape.py, work in progress



import shapes, glob

file_err = []
shape_err = []
cons_err = []
unexp_err = []
family_err=[]

out=open('/home/ejank/Dropbox/comp2ss/outputs/test_rep_struct', 'w')


def unshape(node, file_err=[], shape_err=[], cons_err=[], unexp_err=[], family_err=[]):
	rep_id = ''
	rfam, shape_ss = node.split('_')[0], node.split('_')[1].strip()
	#print rfam, shape_ss
	try:
		with open('/home/ejank/Dropbox/comp2ss/nodes/%s_out' % rfam, 'r') as inp:
				
			for line in inp:
				starts=''
				#print a
				#if a=='':
				#	break
				#print line.split('\t')[5].strip()
				#print line
				if line.split('\t')[5].strip()==shape_ss:
					starts = line.split('\t')[1]
					#print 'starts: ', starts
					break

	except:
		print 'No such output file'
		if rfam in file_err:
			pass
		else:
			file_err.append(rfam)
		return

	if starts=='':
		for filename in glob.glob('/home/ejank/Dropbox/comp2ss/nodes/*_out'):
			#print filename.split('/')[-1]
			with open(filename) as inp:
				for line in inp:
					if (line.split('\t')[5].strip()==shape_ss and line.split('\t')[2].strip()==rfam):
						starts = line.split('\t')[3]
						#print 'starts: ', starts
						break
				else:
					continue  # executed if the loop ended normally (no break)
   				break 
		

	'''

	with open('/home/ejank/Dropbox/comp2ss/outputs/rfamv12_clean_ss_seq.txt', 'r') as seq:
		
		for line in seq:
			
			if line.split('\t')[0]==rfam:
				sequence = line.split('\t')[2].strip()
				structure = line.split('\t')[1].strip()
				#print  'seq: ', sequence, ', ss: ', structure
				break
			else:
				continue
	'''
	
	with open('/home/ejank/Dropbox/comp2ss/outputs/rfamv12_clean_ss_seq.txt', 'r') as seq:
		rfam_dic = {}
		for line in seq:
			rfam_dic[line.split('\t')[0]] = (line.split('\t')[1], line.split('\t')[2]) #dictionary of rfam consensus sequences and structures
			

	with open('/home/ejank/Dropbox/comp2ss/outputs/sequence_representatives', 'r') as seq:
		
		for line in seq:
			#print line
			rep_id=line.split('\t')[0].strip('>')
			print rep_id
			sequence = line.split('\t')[1].strip()
			structure = rfam_dic[rep_id.split('_')[0]][0]
			
			print sequence.replace('-', '')
			print structure
			if len(sequence.replace('-', '')) ==len(structure):
				print 'yay'

			try:	#here actual unshaping happens
				unshape = shapes.smart_sequence(rfam, sequence, structure)
				print starts
				starts =  starts.strip('[').strip(']').split(', ')
				#print starts, len(starts)
				for ind, element in enumerate(starts):
					#print 'element: ', element
					a = unshape.shape_to_seq(int(element), int(element)+len(shape_ss)-1)
					struct_start = unshape.shape_start(int(element))
					struct_end = struct_start+len(a)
					struct_unshaped = structure[struct_start : struct_end] 
		
					#out.write('>%s_%s_%i\n%s\n' % (rfam, shape_ss, ind, struct_unshaped)) #uncomment this if you want unshaped structures as output 
					#print a
					out.write('>%s_%s_%i\n%s\n' % (rfam, shape_ss, ind, a)) #uncomment this if you want unshaped sequences as output
					'''
			except IndexError:
				print 'Shape error'
				if rfam in shape_err:
					pass
				else:
					shape_err.append(rfam)
					'''
			except UnboundLocalError:
				print 'No "starts"'
				if rfam+'.sto' in glob.glob("/home/ejank/klastrowanie/rfam.seed.12.0/*.sto"):
					if rfam in cons_err:
						pass
					else:
						cons_err.append(rfam)
				else:
					if rfam in family_err:
						pass
					else:
						family_err.append(rfam)
	'''
	except:
		print 'Unexpected eror'
		if rfam in unexp_err:
			pass
		else:
			unexp_err.append(rfam)
	'''
def run_unshape(path_to_file):

	with open('%s' % path_to_file, 'r') as nodes:

		for line in nodes:
			if len(line.split('_'))!=2:
				continue
			node = line.strip().strip(' ')
			#print node
			unshape(node, file_err, shape_err, cons_err, unexp_err, family_err)



#test = ['RF01232_()()', 'RF01232_()()', 'RF01571_()()']

#for el in test:
#	unshape(el)



run_unshape('/home/ejank/Dropbox/comp2ss/outputs/all_nodes.csv')

print 'file_err: ', len(file_err), ', shape_err: ', len(shape_err), ', cons_err: ', len(cons_err), ', family_err: ', len(family_err), ', unexp_err: ', len(unexp_err)




'''
out=open('/home/ejank/Dropbox/comp2ss/outputs/error_list', 'w')


out.write('No such output file\n')
for element in file_err:
	out.write('%s\n' % element)


out.write('Error in shape module\n')
for element in shape_err:
	out.write('%s\n' % element)


out.write('No consensus sequence available\n')
for element in cons_err:
	out.write('%s\n' % element)

out.write('No such family\n')
for element in family_err:
	out.write('%s\n' % element)

out.write('Other error\n')
for element in unexp_err:
	out.write('%s\n' % element)
'''












