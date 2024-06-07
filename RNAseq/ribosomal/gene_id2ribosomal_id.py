import re
import sys

name_dic = {}
with open("ribosomal_gene_id",mode='rt') as fh:
    for line in fh:
        if line.startswith('Geneid'):
            continue
        record = re.split("\t",line.strip())
        name_dic[record[0]] = record[1]

count_file = sys.argv[1] # all.counts.txt
result_dic = {}
with open(count_file, mode='rt') as fh,open("all.counts.new.txt", mode='wt') as out:
    for line in fh:
        if line.startswith('Geneid'):
            out.write(line+'\n')
            continue
        record = re.split("\t",line.strip())
        if record[0] in name_dic:
            record[0] = name_dic[record[0]]
        out.write("\t".join(record)+'\n')

