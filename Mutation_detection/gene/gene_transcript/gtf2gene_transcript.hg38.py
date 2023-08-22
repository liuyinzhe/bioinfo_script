import json
import re
import os
import gzip
from pathlib import Path


def parse_info(input_string):
    '''
    AC=1;AF=0.5;AN=2;BaseQRankSum=-0.17;DP=309;ExcessHet=0;FS=0.634;MLEAC=1;MLEAF=0.5;MQ=60;MQRankSum=0;QD=16.1;ReadPosRankSum=0.554;SOR=0.601 
    gtf
    gene_id "DDX11L1"; transcript_id "NR_046018.2"; db_xref "GeneID:100287102"; gbkey "misc_RNA"; gene "DDX11L1"; product "DEAD/H-box helicase 11 like 1 (pseudogene)"; pseudo "true"; transcript_biotype "transcript"; 
    '''
    #print(input_string)
    info_dic = {}
    if ' ' not in input_string :
        return info_dic
    for info_tmp in re.split("; ",input_string):
        #print('#'+info_tmp+'#')
        if ' ' not in info_tmp:
            continue
        keys,value = re.split(' ',info_tmp,maxsplit=1)
        value = re.sub('\"','',value)
        info_dic[keys] = value
    return info_dic

NC2chr_dic = {}
with open('hg38.index',mode='rt',encoding='utf-8') as fh:
    for line in fh:
        if not  line.strip():
            continue
        record = re.split('\t',line.strip())
        NC_id = record[0]
        chr_id = record[1]
        NC2chr_dic[NC_id]=chr_id

with gzip.open('GCF_000001405.40_GRCh38.p14_genomic.gtf.gz',mode='rt',encoding='utf-8') as fh, \
    open('gene_transcript.hg38.tsv',mode='wt',encoding='utf-8') as out:
    out.write('#refseq\tACC\ttranscript\ttranscript_len\n')
    for line in fh:
        if line.startswith('#'):
            continue
        if line.startswith("NC"):
            #print(line)
            '''
            NC_000001.10	BestRefSeq	transcript	11874	14409	.	+	.	gene_id "DDX11L1"; transcript_id "NR_046018.2"; db_xref "GeneID:100287102"; gbkey "misc_RNA"; gene "DDX11L1"; product "DEAD/H-box helicase 11 like 1 (pseudogene)"; pseudo "true"; transcript_biotype "transcript"; 
            '''
            record = re.split('\t',line.strip())
            NC_chr=record[0]
            chr_id = NC2chr_dic[NC_chr]
            start = record[3]
            end = record[4]
            transcript_len = int(end) - int(start)
            info_type=record[2]
            info = record[8]
            if info_type != 'transcript':
                continue
            parse_dic = parse_info(info)
            #print(parse_dic.keys())
            #print(parse_dic['gene_id'],parse_dic['transcript_id'])
            transcript = parse_dic['transcript_id']
            acc = re.split('\.',transcript)[0]
            out.write('\t'.join([parse_dic['gene_id'],acc,transcript,str(transcript_len)])+'\n')
