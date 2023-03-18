import json
import os,re
from pathlib import Path
import pandas as pd



def main():
    name='rno'
    ## 跳转脚本所在目录
    pwd = os.path.split(os.path.realpath(__file__))[0]
    print(pwd)
    #pwd = os.getcwd()
    pwd = Path(pwd)
    os.chdir(pwd)
    
    LV2_dic = {}
    with open(name+"00001.keg",mode='rt',encoding='utf-8') as fh:
        class_type = ""
        for line in fh:
            #print(line)
            if line.startswith("D") or line.startswith("#") or line.startswith("%") or line.startswith("!"):
                continue
            #print('xxx')
            if line.startswith("A") and len(line)>2:
                record = re.split("\s+?",line.strip(),maxsplit=1)
                class_type = record[1]
                print(class_type)
                continue
            if "[PATH:" in line:
                #print(line)
                match_obj = re.search("\[PATH\:(\w{3,})\]",line.strip())
                result_str = match_obj.group(1)
                #print(result_str)
                if result_str not in LV2_dic:
                    LV2_dic[result_str] = class_type


    up_geneid_lst = []
    down_geneid_lst = []
    with open("differential_gene.tsv",mode='rt',encoding='utf-8') as fh:
            for raw_line in fh:
                line= re.sub('\"','',raw_line.strip())
                if line.startswith("GeneId"):
                    continue
                '''
                "GeneId"	"baseMean"	"log2FoldChange"	"lfcSE"	"stat"	"pvalue"	"padj"	"color"
                    0            1             2               3       4        5          6       7
                '''
                record = re.split('\t',line)
                geneid = record[0]
                gene_type = record[7]
                if gene_type == "Up":
                    up_geneid_lst.append(geneid)
                elif gene_type == "Down":
                    down_geneid_lst.append(geneid)
                else:
                    continue
            
    top_num = 9999*2
    all_GO_info = []
    '''
    description(LV2),significance,class(LV1),gene_count,pvalue
    '''
    with open("KEGG_enrich.tsv",mode='rt',encoding='utf-8') as fh:
        for raw_line in fh:
            line= re.sub('\"','',raw_line.strip())
            if line.startswith("ID"):
                    continue
            record = re.split('\t',line)
            '''
            "ID"	"Description"	"GeneRatio"	"BgRatio"	"pvalue"	"p.adjust"	"qvalue"	"geneID"	"Count"
            0            1           2              3          4          5            6          7           8 
            '''
            description = record[1]
            pvalue = float(record[4])
            geneid = record[7]
            geneid_lst = re.split("/",geneid)
            kegg_ID = record[0]
            if kegg_ID not in LV2_dic:
                #print(kegg_ID)
                continue
            kegg_class = LV2_dic[kegg_ID]

            gene_count = int(record[8])
            up_gene_count = 0
            down_gene_count = 0
            for gene_id in geneid_lst:
                #print(gene_id)
                if gene_id in up_geneid_lst:
                    up_gene_count+=1
                elif gene_id in down_geneid_lst:
                    down_gene_count+=1
            all_GO_info.append([description,kegg_class,"up",up_gene_count,pvalue,gene_count])
            all_GO_info.append([description,kegg_class,"down",down_gene_count,pvalue,gene_count])
        all_KEGG_sorted = sorted(all_GO_info,key=lambda x:(x[4],-x[5]))

    count = 0
    with open("KEGG_bar_plot.tsv",mode='wt',encoding='utf-8') as out:
        out.write('description\tkegg_class\tsignificance\tgene_count\n')
        for x in all_KEGG_sorted:
            count +=1
            print(count,x)
            out.write('\t'.join(list(map(str,x[0:4])))+'\n')
            if count == top_num:
                break
        
if __name__ == '__main__':
    main()
