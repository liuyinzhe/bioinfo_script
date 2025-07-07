import pickle
import re

def parse_info(input_string):
    '''
    ID=ENST00000270722.10;Parent=ENSG00000142611.17;gene_id=ENSG00000142611.17;transcript_id=ENST00000270722.10;gene_type=protein_coding;gene_name=PRDM16;transcript_type=protein_coding;transcript_name=PRDM16-201;tag=MANE_Select;protein_id=ENSP00000270722.5;Dbxref=RefSeq:NM_022114.4
    '''
    #print(input_string)
    info_dic = {}
    if '=' not in input_string :
        return info_dic
    for info_tmp in re.split(";",input_string):
        #print('#'+info_tmp+'#')
        if '=' not in info_tmp:
            continue
        keys,value = re.split('=',info_tmp,maxsplit=1)
        info_dic[keys] = value
    return info_dic

def main():
    # 获取常用 转录本
    MANE_transcript_dic = {}
    with open('/data/home/liuyinzhe/project/dev/MANE/MANE.GRCh38.v1.4.ensembl_genomic.gff',mode='rt', encoding='utf-8') as fh:
        '''
        #chr1    ensembl_havana  transcript      3069203 3438621 .       +       .       
        # ID=ENST00000270722.10;Parent=ENSG00000142611.17;
        # gene_id=ENSG00000142611.17;transcript_id=ENST00000270722.10;
        # gene_type=protein_coding;gene_name=PRDM16;
        # transcript_type=protein_coding;transcript_name=PRDM16-201;
        # tag=MANE_Select;protein_id=ENSP00000270722.5;Dbxref=RefSeq:NM_022114.4
        '''
        for line in fh:
            if line.startswith("#"):
                continue
            record = re.split("\t",line.strip())
            gene_type = record[2] # transcript
            info_str = record[8]
            #print(gene_type)
            if gene_type == "transcript":
                info_dic = parse_info(info_str)
                gene_name = info_dic["gene_name"]
                tag = info_dic["tag"]#tag=MANE_Select
                Dbxref_str = info_dic["Dbxref"]#Dbxref=RefSeq:NM_022114.4
                refseq_transcript_dot = re.split(":",Dbxref_str)[-1]
                refseq_transcript = re.split("\.",refseq_transcript_dot)[0]
                if tag == "MANE_Select":
                    MANE_transcript_dic[gene_name] = [refseq_transcript,refseq_transcript_dot]

    print(MANE_transcript_dic)
    pickle.dump(MANE_transcript_dic, open("MANE_transcript.hg38.pkl", 'wb'))

    # # 反序列化
    # MANE_transcript_dic = pickle.load(open("MANE_transcript.pkl", 'rb'))
    # print(MANE_transcript_dic)


if __name__ == '__main__':
    main()


