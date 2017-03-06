'''
Usage: ./RNAforester [options]
--help                    shows this help info
--version                 shows version information
-f=file                   read input from file
--score                   compute only scores, no alignment
--noscale                 suppress output of scale
--tables                  shows dynamic programming tables
--backtrace               shows backtrace call table cells
-t                        calculate alignment top down instead of bottom up
-d                        calculate distance instead of similarity
-r                        calculate relative score
-l                        local similarity
-so=int                   local suboptimal alignments within int%
-s                        small-in-large similarity
--anchor                  use shape anchoring for speedup
-a                        affine gap scoring
-m                        multiple alignment mode
--RIBOSUM                 RIBOSUM85-60 scoring matrix (base-pair substitutions)
-cbmin=double             minimum base frequency for consensus structure
-cmin=double              minimum basepair frequency for consensus structure
-mt=double                clustering threshold
-mc=double                clustering cutoff
-sp=file                  save profile
-ps=file                  profile search
-pm=int                   basepair(bond) match score
-pd=int                   basepair bond indel score
-pdo=int                  basepair bond indel open score
-bm=int                   base match score
-br=int                   base mismatch score
-bd=int                   base indel score
-bdo=int                  base indel open score
-2d                       generate alignment 2D plots in postscript format
--2d_hidebasenum          hide base numbers in 2D plot
--2d_basenuminterval=n    show every n-th base number
--2d_grey                 use only grey colors in 2D plots
--2d_scale=double         scale factor for the 2d plots
--2d_fig                  generate additional fig file of 2d plot
--fasta                   generate fasta output of alignments

'''

# 

#set1 -l -pd=-20 -bm=0 -bd=-20 
#set2 -l -bm=0
#set3 -l -a -pd=-20 -pdo=-20 -bm=0 -bd=-1 -bdo=-20 
#set4 -l -a -pd=-20 -pdo=-20 -bm=0 -bd=-1 -bdo=-1 

#forester1 -l -pd=-20 -bm=0 -bd=-20 these stringent parameters were used to search for common local motifs

#forester2 -l -pd=-20 -bm=0 -bd=-1 -bdo=-10

###author: Staszek

import sys, subprocess


def runfile(filename):

	resfile = open(filename+'_global.res', 'w')

	f=open(filename)
	l1=f.readline()
	while l1:
		l2=f.readline()
		rfam1, ss1 = l1.split('\t')
		rfam2, ss2 = l2.split('\t')
		seq1 = 'a'*len(ss1)
		seq2 = 'a'*len(ss2)

		assert rfam1<>rfam2
		
		#print rfam1, rfam2
		#print ss1
		#print ss2
				#when comparing structures of local motifs we use global similarity and default parameters
		command = """/home/ejank/Soft/RNAforester-2.0/src/RNAforester --fasta --noscale -r << eof 
>%(rfam1)s
%(seq1)s
%(ss1)s
>%(rfam2)s
%(seq2)s
%(ss2)s
eof
""" % locals()
		
		
	

		# uwaga: w zaleznosci od uzytych opcji RNAforster zwraca output roznej dlugosci, wiec koniczne moze byc pozmienianie numerkow poznizej
		
		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		
		forres = proc.communicate()[0].split('\n')

		#FIXME
		if len(forres)<14: 
			l1=f.readline()
			continue
		
		print command
		for i,x in enumerate(forres): print i,x
		

		if forres[12].find("Alignment computation aborted, out of memory.")<>-1: 
			l1=f.readline()
			continue

		# no -a option
		score = forres[10].split(":")[-1].strip()
		rel_score = forres[11]
		seq1 = forres[14]
		ss1 = forres[15]	
		seq2 = forres[17]
		ss2 = forres[18]

		# -a option

                #score = forres[12].split(":")[-1].strip()
                #seq1 = forres[16]
                #ss1 = forres[17]
                #seq2 = forres[19]
                #ss2 = forres[20]

		
		print >>resfile, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (rfam1, rfam2, seq1, seq2, ss1, ss2, score, rel_score)
		
		#print forres[15]
		#print forres[18]

		#print
		
		l1=f.readline()
		
	resfile.close()
		
		
	
if __name__ == '__main__':
	print sys.argv[1]
	
	runfile(sys.argv[1])


### Do puszczania na klastrze
# for x in *.txt; do echo "python /home/ejank/forester/Scripts/rfam2ss_run.py $x" | qsub -cwd -V -l h_vmem=4GB; done

### Do puszczania na lokalnym komputerze z folderu w ktorym sa pliki do forestera
# for x in *.txt; do python /home/ejank/klastrowanie/Scripts/rfam2ss_run.py $x; done



