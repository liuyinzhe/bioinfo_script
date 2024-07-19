import re
import os
import pandas as pd

#os.chdir(r'D:\Rscript\Net4\format')

'''
拆分为两组文件
一个根据纲目科属种分类
kingdom,phylum,class,order,family,genus,species
界，门，纲，目，科，属，种
0   1   2   3   4   5   6

植物界（plant kingdom）0
门（divisio）   1 Phylum
纲（classis）2
目（ordo）3
科（familia）4
属（genus）5
种（species）6

输出以下列
phylum,class,order,family,genus,species
 1       2    3      4      5     6
一个根据样品丰度统计
OTU_ID
'''


def parse_taxonomy(taxonomy_str):
    '''

    # kingdom,phylum,class,order,family,genus,species
    #  0     , 1   , 2   ,3     ,  4     ,5   ,6
    #  1        2      3     4     5      6     7

    D_0__Bacteria; D_1__Firmicutes; D_2__Clostridia; D_3__Clostridiales; D_4__Christensenellaceae; D_5__Christensenellaceae R-7 group
    D_0__Bacteria; D_1__Bacteroidetes; D_2__Bacteroidia; D_3__Bacteroidales; D_4__Muribaculaceae; D_5__uncultured bacterium; D_6__uncultured bacterium
    '''
    records = re.split(';',taxonomy_str.strip())
    taxonomy_type = ['phylum','class','order','family','genus','species']
    taxonomy_lst = []
    #print(records)
    for index in range(len(taxonomy_type)+1):
        #print(index)
        if index==0:
            continue
        if index < len(records):
            match_obj = re.search(r"D_"+str(index)+"__(.+)",records[index].strip())
            if match_obj :
                taxonomy_info = match_obj.group(1)
                if "[" in taxonomy_info:
                    taxonomy_info = re.split("[\[\]]",taxonomy_info)[1]
                taxonomy_info = re.sub('\s','_',taxonomy_info.strip())
                taxonomy_lst.append(taxonomy_info)
            else:
                print("Warring!：not match:\t\""+records[index]+"\"\n")
                taxonomy_lst.append('NA')
        else: # 超出范围
            taxonomy_lst.append('NA')
    #print(records)
    #print(taxonomy_lst)
    return taxonomy_lst


pwd = os.path.split(os.path.realpath(__file__))[0]
os.chdir(pwd)

line_lst = []
taxonomy_lst = []
with open('otu_table.txt',mode='rt',encoding='utf-8') as fh, open('otu_table_D5.csv',mode='wt',encoding='utf-8') as otu:
    for line in fh:
        if line.startswith('# Constructed'):
            continue
        elif line.startswith('#OTU ID'):
            # otu_table.csv
            header = re.sub('#OTU ID','OTU_ID',line.strip())
            otu.write(header+"\n")
            continue

        # otu_table.csv
        records = re.split('\t',line.strip())
        # otu_taxonomy.csv
        taxonomy_str = records[-1]
        phylum,class_info,order,family,genus,species = parse_taxonomy(taxonomy_str)
        if species == "NA" and genus != "NA":
            records[-1] = genus
        else:
            continue
        otu.write('\t'.join(records)+'\n')

with open('otu_table_D5.csv',mode='rt',encoding='utf-8') as fh,open('otu_table_D5_input.tsv',mode='wt',encoding='utf-8') as otu:
    taxonomy_dict = {}
    taxonomy_lst = []
    for line in fh:
        records = re.split("\t",line.strip())
        if line.startswith("OTU_ID"):
            otu.write('taxonomy\t'+"\t".join(records[1:-1])+'\n')
            continue
        int_lst = list(map(float,records[1:71]))
        taxonomy_key = records[-1]
        taxonomy_lst.append(taxonomy_key)
        if taxonomy_key not in taxonomy_dict:
            taxonomy_dict[taxonomy_key] = int_lst
        else:
            for index in range(len(int_lst)):
                #print(taxonomy_dict[taxonomy_key][index])
                taxonomy_dict[taxonomy_key][index] += int_lst[index]
                #print('#',taxonomy_dict[taxonomy_key][index])
    
    for taxonomy_key in set(taxonomy_lst):
        new_lst = list(map(int,taxonomy_dict[taxonomy_key]))
        new_lst2 = list(map(str,new_lst))
        #print(new_lst2)
        print(len(new_lst2))
        otu.write(taxonomy_key+'\t'+'\t'.join(new_lst2)+"\n")




df = pd.read_csv('otu_table_D5_input.tsv',sep='\t',names=[
    "NO1","NO2","NO3"])# 
new_df = df.T

print(new_df)
# 指定排序
# new_df['taxonomy'].astype('category')
# new_df['taxonomy'].cat.set_categories([],inplace=True)

new_df.to_csv('otu_table_D5_out.tsv',sep='\t',index=False)#index=False,columns=['NO12-1','NO12-2']


with open('otu_table_D5_out.tsv',mode='rt',encoding='utf-8') as fh,\
    open('otu_table_D5_no1.tsv',mode='wt',encoding='utf-8') as outn1,\
    open('otu_table_D5_no2.tsv',mode='wt',encoding='utf-8') as outn2:
    for line in fh:
        records = re.split('\t',line.strip())
        if line.startswith('taxonomy'):
            outn1.write(line)
            outn2.write(line)
            continue
        if re.search("^NO\d+?-1",line):
            line = re.sub("-1","",line)
            outn1.write(line)
        elif re.search("^NO\d+?-2",line):
            line = re.sub("-2","",line)
            outn2.write(line)
