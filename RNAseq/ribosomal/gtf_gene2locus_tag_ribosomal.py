import re
import sys


def info2dic(info_str):
    info_dic = {}
    record = re.split('; ',info_str.strip())
    for field in record:
        item = re.split('\s+',field)
        info_dic[item[0]] = item[1]
    return info_dic


input_gtf = sys.argv[1]
result_dic = {}
with open(input_gtf, mode='rt') as fh,open("locus_tag2gene.tsv", mode='wt') as out,open("ribosomal_gene_id",mode='wt') as ribosomal:
    for line in fh:
        if line.startswith('#'):
            continue
        record = re.split("\t",line.strip())
        if record[2] == "gene":
            info_str = record[0]
            info_dic = info2dic(info_str)
            gene_id = info_dic["gene_id"]
            locus_tag = info_dic["locus_tag"]
            if "gene" in info_dic:
                gene = info_dic["gene"]
                result_dic[gene_id] = gene
                out.write("{gene_id}\t{gene}\n".format(gene_id=gene_id,gene=gene))
                if "ribosomal" in info_str:
                    ribosomal.write("{gene_id}\t{gene}\n".format(gene_id=gene_id,gene=gene))
        else:
            continue
