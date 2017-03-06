### This script divides seguences into chunks corresponding to structural features and saves them in separate files

import shapes, glob
import sys, subprocess
import os.path

file_err = []
shape_err = []
cons_err = []
unexp_err = []
family_err=[]

out=open('/home/ejank/Dropbox/comp2ss/unshape_test/nodes_unshaped', 'w')


def unshape(node, file_err=[], shape_err=[], cons_err=[], unexp_err=[], family_err=[]):
	write = ''
	rfam, shape_ss = node.split('_')[0], node.split('_')[1].strip()
	print rfam, shape_ss
	try:
		with open('/home/ejank/Dropbox/comp2ss/nodes/%s_out' % rfam, 'r') as inp:
				
			for line in inp:
			
				#print a
				#if a=='':
				#	break
				#print line.split('\t')[5].strip()
				if line.split('\t')[5].strip()==shape_ss:
					starts = line.split('\t')[1]
					print 'starts: ', starts
					break
	except:
		print 'No such output file'
		if rfam in file_err:
			pass
		else:
			file_err.append(rfam)
		
	with open('/home/ejank/Dropbox/comp2ss/outputs/rfamv12_clean_ss_seq.txt', 'r') as seq:
		
		for line in seq:
			
			if line.split('\t')[0]==rfam:
				sequence = line.split('\t')[2].strip()
				structure = line.split('\t')[1].strip()
				print  'seq: ', sequence, ', ss: ', structure
				break
			else:
				continue

	try:
		unshape = shapes.smart_sequence(rfam, sequence, structure)

		starts =  starts.strip('[').strip(']').split(', ')

		print starts
		for ind, start in enumerate(starts):
			for index, sign in enumerate(shape_ss):
				
				a = unshape.shape[int(start)+index: int(start)+index+1][0][1]
				#a = unshape.shape_to_seq(int(start)+index, int(start)+index+1)
				#a = unshape.shape_to_seq(int(element), int(element)+len(shape_ss)-1)
				
				if write == open('/home/ejank/Dropbox/comp2ss/unshape_test/parts/out_%i' % index, 'a'): #os.path.exists('/home/ejank/Dropbox/comp2ss/unshape_test/parts/out_%i' % index) == True:
					write.write('>%s_%s_%i\n%s\n' % (rfam, shape_ss, ind, a))
				else:
					write = open('/home/ejank/Dropbox/comp2ss/unshape_test/parts/out_%i' % index, 'a')
					write.write('>%s_%s_%i\n%s\n' % (rfam, shape_ss, ind, a))
				print a
			#out.write('>%s_%s_%i\n%s\n' % (rfam, shape_ss, ind, a))
		
	except IndexError:
		print 'Shape error'
		if rfam in shape_err:
			pass
		else:
			shape_err.append(rfam)
	
	except UnboundLocalError:
		print 'No consensus sequence'
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
	
			
	except:
		print 'Unexpected eror'
		if rfam in unexp_err:
			pass
		else:
			unexp_err.append(rfam)
	
def run_unshape(path_to_file):

	with open('%s' % path_to_file, 'r') as nodes:

		for line in nodes:
			if len(line.split('_'))!=2:
				continue
			node = line.strip().strip(' ')
			#counter = len(line.strip().strip(' ')
			print node
			unshape(node, file_err, shape_err, cons_err, unexp_err, family_err)
			#shape_ss = node.split('_')[1].strip()
			#for ind, sign in enumerate(shape_ss):
			#	out = open('/home/ejank/Dropbox/comp2ss/unshape_test/parts/out_%i' % ind, 'w')
			#	out.close()



run_unshape('/home/ejank/Dropbox/comp2ss/unshape_test/node_0.csv')

print 'file_err: ', len(file_err), ', shape_err: ', len(shape_err), ', cons_err: ', len(cons_err), ', family_err: ', len(family_err), ', unexp_err: ', len(unexp_err)








