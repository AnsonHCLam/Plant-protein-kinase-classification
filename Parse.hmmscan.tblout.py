import math
import argparse

parser = argparse.ArgumentParser(description = 'summary hmmscan results')
parser.add_argument('results', help='target tblout output file of hmmscan')

args = parser.parse_args()


target_file = open(args.results, 'r')

hit={}

for line in target_file.readlines():
    if line[0] != '#':
        sline = str.split(line)
        if sline[2] not in hit.keys():
            hit[sline[2]]=[[sline[0], sline[4]]]
        elif len(hit[sline[2]]) == 1:
            hit[sline[2]].append([sline[0], sline[4]])

for gene in hit.keys():
    E1=float(hit[gene][0][1])
    
    if len(hit[gene]) == 2:
        E2=float(hit[gene][1][1])
        if E2 != 0:
            if E1/E2 > 0:
                hit[gene].append(-math.log10(E1/E2))
            
out = str(args.results[:-4] + '_summary.txt')
target_out = open(out, 'w')

for gene in hit.keys():
    if len(hit[gene]) == 3:
        target_out.write(gene + '\t' + hit[gene][0][0] + '\t' + hit[gene][0][1] + '\t' + hit[gene][1][0] + '\t' + hit[gene][1][1] + '\t' + str(hit[gene][2]) + '\n')
    elif len(hit[gene]) == 2:
        target_out.write(gene + '\t' + hit[gene][0][0] +'\t' + hit[gene][0][1] + '\t' + hit[gene][1][0] + '\t' + hit[gene][1][1] + '\n')
    elif len(hit[gene]) == 1:
        target_out.write(gene + '\t' + hit[gene][0][0] +'\t' + hit[gene][0][1] + '\n')
        
target_file.close()
target_out.close()


parsed_out = open(out, 'r')

hit2 = {}

for line in parsed_out.readlines():
    sline = str.split(line, '\t')
    if sline[1] not in hit2.keys():
        hit2[sline[1]] = 1
    else:
        hit2[sline[1]] += 1

count = []
j=0
for i in hit2.keys():
    count.append([i, hit2[i]])
print(count)

count_ordered = sorted(count, key = lambda count:count[1], reverse = True)

out_count = str(out[:-4]+'_count.txt')
summary = open(out_count, 'w')

for i in range(len(count_ordered)):
    summary.write(str(count_ordered[i][0]) + '\t' + str(count_ordered[i][1]) + '\n')

parsed_out.close()
summary.close()