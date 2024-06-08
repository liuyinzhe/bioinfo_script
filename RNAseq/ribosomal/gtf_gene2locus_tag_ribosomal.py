import re
import sys


def info2dic(info_str):
    info_dic = {}
    record = re.split('; ',info_str.strip())
    for field in record:
        field = re.sub('"',"",field)
        item = re.split('\s+',field)
        #print(item)
        info_dic[item[0]] = item[1]
    return info_dic


input_gtf = sys.argv[1]
result_dic = {}
ribosomal_dic = {}
with open(input_gtf, mode='rt') as fh,open("locus_tag2gene.tsv", mode='wt') as out,open("ribosomal_gene_id",mode='wt') as ribosomal:
    for line in fh:
        if line.startswith('#'):
            continue
        record = re.split("\t",line.strip())
        if record[2] == "gene":
            info_str = record[8]
            #print(record[8])
            info_dic = info2dic(info_str)
            gene_id = info_dic["gene_id"]
            locus_tag = info_dic["locus_tag"]
            if "gene" in info_dic:
                gene = info_dic["gene"]
                result_dic[gene_id] = gene
                out.write("{gene_id}\t{gene}\n".format(gene_id=gene_id,gene=gene))
        else:
            if  "ribosomal" in line:
                info_str = record[8]
                info_dic = info2dic(info_str)
                if 'gene' not in info_dic:
                    continue
                gene_id = info_dic["gene"]
                locus_tag = info_dic["locus_tag"]
                ribosomal_dic[locus_tag] = gene_id
    ##
    for locus_tag in  ribosomal_dic:
        gene_id = ribosomal_dic[locus_tag]
        ribosomal.write("{locus_tag}\t{gene_id}\n".format(locus_tag=locus_tag,gene_id=gene_id))


