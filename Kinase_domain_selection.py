# modules
import argparse

# import arguments and options
parser = argparse.ArgumentParser(description = 'extract kinase sequences belonging to a family')
parser.add_argument('fasta', help = 'fasta file')
parser.add_argument('hmmscan', help = 'hmmscan tblout result processed with Parsed.hmmscan.tblout.py (tsv)')
parser.add_argument('family', help = 'name of kinase family you want to extract. e.g. RLK-Pelle...')
parser.add_argument('output_fa', help = 'name of output fa file')

args = parser.parse_args()

# import protein sequence (FASTA)
fasta_file = open(args.fasta, 'r')

ID_sequence = {}

for line in fasta_file.readlines():
    if len(line) > 0:
        if line[0] == '>':
            ID = str.split(line, ' ')[0][1:]
            ID_sequence[ID] = ''
        
        else:
            if len(str.split(line)) > 0:
                ID_sequence[ID] += str.split(line)[0]

fasta_file.close()


# associate gene with kinase family
gene_family = {}
hmmscan_out = open(args.hmmscan, 'r')

for line in hmmscan_out.readlines():
    sline = str.split(line, '\t')
    gene_family[sline[0]] = sline[1] 

hmmscan_out.close() 

# export genes with domain
fasta_output = open(args.output_fa, 'w')

count = 0

for gene in gene_family.keys():
    if gene_family[gene] == args.family:
        fasta_output.write('>' + gene + ' ' + gene_family[gene] + '\n')
        fasta_output.write(ID_sequence[gene] + '\n')
        count += 1

fasta_output.close()
print('exported ' + str(count) + ' ' + args.family + ' sequences') 
