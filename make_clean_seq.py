### This script generates a single file containing rfams sequences and structures without non-representative bulges, for use for comp2ss.py
### and prepares files for RNAforester comparison
### input - rfam seed alignments in stockholm format, output - a file with all rfam families, in each line a rfamid, secondary structure in shape format and sequence

from Bio import AlignIOsdh as AlignIO
import glob, itertools, os, sys, subprocess, numpy, copy, string


def find_sequence(text): #extracting the consensus secondary structure line from the alignment
	seq = ''
	for line in text:
		if line.startswith('#=GC RF'):
			line = string.strip(line, '#=GC RF')
			line = string.strip(line)
			seq = seq + line
	return seq


def clean_alignment(filename, ss, seq): #removing non-representative bulges from consensus structures. Author: Ela

	align = AlignIO.read(filename, "stockholm")
	#print align
	delete=[]
	for i in range(0, len(align[1])):
		column = align[: , i]
		if column.count('-') > len(column)//2:
			delete.append(i)

	#print delete
	
	clean=[]
	clean_seq=[]
	deleted=[]
	for ind, el in enumerate(ss):
		if (ind in delete and el=='.'):
			deleted.append(ind)
			continue
		clean.append(el)
		
	clean=''.join(clean)

	for ind, el in enumerate(seq):
		if ind in deleted:
			continue
		clean_seq.append(el)

	clean_seq=''.join(clean_seq)

	return (clean, clean_seq)


 


def dofiles():#filepath):#maxsslen=None):
	"""
	
	przygotowywuje sekwencje do puszczania RNAforestera na klastrze
	
	maxsslen - maksymalna dlugosc sekwencji (zeby np. nie brac rRNA itp.)
	
	"""
	ss_structs = []
	norf = open('/home/ejank/Dropbox/forester/outputs/rfamsv12_with_no_RF.txt', 'w')
	clean_seqs=open('/home/ejank/Dropbox/forester/outputs/rfamv12_clean_ss_seq.txt', 'w')
	i=0

	for sto in glob.glob("/home/ejank/klastrowanie/rfam.seed.12.0/*.sto"):

		#sto=filepath
		rfamid = sto.split('/')[-1].split('.')[0]
		print rfamid
		#seq = find_sequence(sto)
		#if rfamid == 'RF02221' or rfamid=='RF00773' or rfamid=='RF01169':
		#	continue		

		alignment = list(AlignIO.parse(sto, 'stockholm'))[0]

		if 'RF' not in alignment._annotations.keys():
			print >> norf, (rfamid)	
			continue	

		ss=alignment._annotations['SS_cons']
		seq=alignment._annotations['RF']
		
		i=i+1

		print "%s\t%s" % (rfamid, alignment._annotations["ID"][0])

		ss = ss.replace("<", "(").replace(">", ")").replace("a", ".").replace("A", ".").replace("b", ".").replace("B", ".").replace("c", ".").replace("C", ".").replace("d", ".").replace("D", ".").replace(':', '.').replace('_', '.').replace('-','.').replace(',', '.').replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")")
		#print ss
		aln = clean_alignment(sto, ss, seq)
		ss, seq = aln[0], aln[1]
		print aln
		#ss = ss.replace('()', '(...)').replace('(.)', '(...)').replace('(..)', '(...)').replace('....', '.')
		seq = seq.upper()
		print >> clean_seqs, ("%s\t%s\t%s" % (rfamid, ss, seq))



dofiles()
