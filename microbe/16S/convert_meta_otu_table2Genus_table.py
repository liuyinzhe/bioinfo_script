import pandas as pd
import re

'''
k__Bacteria|p__Firmicutes|c__Bacilli|o__Lactobacillales|f__Streptococcaceae|g__Streptococcus|s__Streptococcus_anginosus_group
TO
D_0__Bacteria; D_1__Firmicutes; D_2__Bacilli; D_3__Lactobacillales; D_4__Streptococcaceae; D_5__Lactococcus; D_6__uncultured bacterium
#  * 10000 取整数
k__Archaea	0	0	0	0	0	0	0	0	0	0	0	0	0	0	2.13877	0.00601	0.01145	0.03142	0.19934000000000002	0.0035600000000000002	
'''

'''
clade_name	ZKRJ040	ZKRJ039	ZKRJ038	ZKRJ037	ZKRJ036	ZKRJ035	ZKRJ018	ZKRJ017	ZKRJ016	ZKRJ015	ZKRJ014	ZKRJ013	ZKRJ012	ZKRJ011	ZKRJ010	ZKRJ009	ZKRJ008	ZKRJ007	ZKRJ006	ZKRJ005	HLJQTH007YB910	HLJQTH007YB78	HLJQTH007YB56	HLJQTH007YB34	HLJQTH007YB12	HLJQTH007TR910	HLJQTH007TR78	HLJQTH007TR56	HLJQTH007TR34	HLJQTH007TR1314	HLJQTH007TR12	HLJQTH007TR1112	HLJQTH007TR015	HLJQTH007TQ789	HLJQTH007TQ456	HLJQTH007TQ123	HLJQTH007TQ101112	HLJQTH007TH789	HLJQTH007TH456	HLJQTH007TH123	HLJQTH007TH101112	HLJQTH007TG910	HLJQTH007TG78	HLJQTH007TG56	HLJQTH007TG34	HLJQTH007TG12	HLJQTH007TG1112	HLJQTH007FN910	HLJQTH007FN78	HLJQTH007FN56	HLJQTH007FN34	HLJQTH007FN12	HLJQTH007FN1112	LYTZLQ9	LYTZLQ8	LYTZLQ7	LYTZLQ6	LYTZLQ5	LYTZLQ4	LYTZLQ3	LYTZLQ2	LYTZLQ12	LYTZLQ1	LYTZLQ11	LYTZLQ10	LYTZLH9	LYTZLH8	LYTZLH7	LYTZLH6	LYTZLH5	LYTZLH4	LYTZLH3	LYTZLH2	LYTZLH12	LYTZLH1	LYTZLH11	LYTZLH10	LYTZGS9	LYTZGS8	LYTZGS7	LYTZGS6	LYTZGS5	LYTZGS4	LYTZGS2	LYTZGS12	LYTZGS1	LYTZGS11	LYTZGS10	LYTZGH9	LYTZGH8	LYTZGH7	LYTZGH6	LYTZGH5	LYTZGH4	LYTZGH3	LYTZGH2	LYTZGH14	LYTZGH13	LYTZGH12	LYTZGH1	LYTZGH11	LYTZGH10	LYFHZF6	LYFHZF5	LYFHZF4	LYFHZF3	LYFHZF2	LYFHZF1	LYFHDN9	LYFHDN8	LYFHDN7	LYFHDN6	LYFHDN5	LYFHDN4	LYFHDN3	LYFHDN2	LYFHDN12	LYFHDN1	LYFHDN11	LYFHDN10	HLJJMS007YB00910	HLJJMS007YB0078	HLJJMS007YB0056	HLJJMS007YB0034	HLJJMS007YB0012	HLJJMS007TQ01012	HLJJMS007TQ0079	HLJJMS007TQ0046	HLJJMS007TQ0013	HLJJMS007TH01012	HLJJMS007TH0079	HLJJMS007TH0046	HLJJMS007TH0013	HLJJMS007TG01012	HLJJMS007TG0079	HLJJMS007TG0046	HLJJMS007TG0013	HLJJMS007FN0013	HLJJMS007FB0056	HLJJMS007FB0034	HLJJMS007FB0012	HBRJ2022142	HBRJ2022141	HBRJ2022140	HBRJ2022139	HBRJ2022138	HBRJ2022137	HBRJ2022136	HBRJ2022135	HBRJ2022134	HBRJ2022133	HBRJ2022132	HBRJ2022131	HBRJ2022130	HBRJ2022129	HBRJ2022128	HBRJ2022115	HBRJ2022114	HBRJ2022113	HBRJ2022112	HBRJ2022111	HBRJ2022110	HBRJ2022109	HBRJ2022108	HBRJ2022107	HBRJ2022106	HBRJ2022105	HBRJ2022104	HBRJ2022065	HBRJ2022064	HBRJ2022054	HBRJ2022053	HBRJ2022052	HBRJ2022051	HBRJ2022050	HBRJ2022049	HBRJ2022022N	HBRJ2022021N	HBRJ2022020N	HBRJ2022019N	HBRJ2022018N	HBRJ2022017N	HBRJ2022016N	HBRJ2022015N	HBRJ2022014N	HBRJ2022013N	HBRJ2022012N	HBRJ2022011N	HBRJ2022010	HBRJ2022009	HBRJ2022008	HBRJ2022007	HBRJ2022006	HBRJ2022005
UNKNOWN	0	0	0	0	0	0	0	0	

TO
# Constructed from biom file
#OTU ID	S39	S73	M101	M102	M141	M142	M71	M171	S63	S67	M131	M62	M172	M41	S12	S14	M72	M112	S42	S27	S75	S66	M31	S40	M111	S65	S76	S58	S13	S64	S62	M132	M272	M252	S29	M121	M261	M251	M42	M61	S35	S28	M32	S41	S38	S43	taxonomy
HM124173.1.1493	0.0	2.0	2.0	30.0
'''


def parse_taxonomy(taxonomy_str):
    '''

    # kingdom,phylum,class,order,family,genus,species
    #  0     , 1   , 2   ,3     ,  4     ,5   ,6
    #  1        2      3     4     5      6     7
    k__Bacteria|p__Firmicutes|c__Bacilli|o__Lactobacillales|f__Streptococcaceae|g__Streptococcus|s__Streptococcus_anginosus_group

    D_0__Bacteria; D_1__Firmicutes; D_2__Clostridia; D_3__Clostridiales; D_4__Christensenellaceae; D_5__Christensenellaceae R-7 group
    D_0__Bacteria; D_1__Bacteroidetes; D_2__Bacteroidia; D_3__Bacteroidales; D_4__Muribaculaceae; D_5__uncultured bacterium; D_6__uncultured bacterium

    D_0__Bacteria; D_1__Firmicutes; D_2__Clostridia; D_3__Clostridiales; D_4__Lachnospiraceae; D_5__Lachnospiraceae FCS020 group; D_6__uncultured bacterium
    D_0__Bacteria; D_1__Firmicutes; D_2__Clostridia; D_3__Clostridiales; D_4__Lachnospiraceae; D_5__Fusicatenibacter; Ambiguous_taxa
    D_0__Bacteria; D_1__Bacteroidetes; D_2__Bacteroidia; D_3__Bacteroidales; D_4__Tannerellaceae; D_5__Parabacteroides
    D_0__Bacteria; D_1__Proteobacteria; D_2__Alphaproteobacteria; D_3__Rhizobiales; D_4__Rhizobiaceae; D_5__Ochrobactrum
                                                                                                           genus
    '''#Ambiguous_taxa
    records = re.split(r"\|",taxonomy_str.strip())
    #print(records)
    taxonomy_type = ['kingdom','phylum','class','order','family','genus','species']
                    #    0        1        2      3         4       5        6
    taxonomy_lst = []
    #print(records)
    for index in range(0,len(taxonomy_type)):
        # if index==0:
        #     continue
        # print(index)
        if index < len(records):
            match_obj = re.search(r"[kpcofgs]__(.+)",records[index].strip())
            if match_obj :
                taxonomy_info = match_obj.group(1)
                if "[" in taxonomy_info:
                    taxonomy_info = re.split("[\[\]]",taxonomy_info)[1]
                taxonomy_info = re.sub('\s','_',taxonomy_info.strip())
                taxonomy_info = "D_"+str(index)+"__"+taxonomy_info
                taxonomy_lst.append(taxonomy_info)
            else:
                print("Warring!：not match:\t\""+records[index]+"\"\n")
                continue
                #taxonomy_lst.append('NA')
        else: # 超出范围
            continue
            #taxonomy_lst.append('NA')
    return taxonomy_lst

dup_otu_id = {}
count = 1
with open('format_abundance.txt',mode='rt',encoding='utf-8') as fh, open('otu_tablex.txt',mode='wt',encoding='utf-8') as out:
    for line in fh:
        record = re.split('\t',line.strip())
        
        if line.startswith('clade_name'):
            new_line = re.sub("clade_name","#OTU ID",line)
            new_line = re.sub("\n","\ttaxonomy\n",new_line)
            out.write(new_line)
            continue
        # 末尾添加一个分类编号
        if r"|" not in  line:  # 只有一个分类 如
            #print(record[0])
            taxonomy = re.sub("k__","D_5__",record[0])
            new_record = list(map(lambda x:str(int(float(x)*10000)),record[1:]))
            out.write(record[0]+'\t'+"\t".join(new_record)+"\t"+taxonomy+"\n")
        else:
            # 解析taxonomy
            taxonomy_str = record[0]
            #print(re.split('\|',taxonomy_str)[-1])
            otu_id = re.split(r"\|",taxonomy_str)[-1]
            print(otu_id)
            # 重复的otu_id 添加序号
            if otu_id not in dup_otu_id:
                dup_otu_id[otu_id] = 1
            else:
                otu_id = otu_id+"_"+str(count)
                count += 1
                dup_otu_id[otu_id] = 1
            #print(taxonomy_str)
            taxonomy_lst = parse_taxonomy(taxonomy_str)
            new_record = list(map(lambda x:str(int(float(x)*10000)),record[1:]))
            out.write(otu_id+"\t"+'\t'.join(new_record)+"\t"+r";".join(taxonomy_lst)+"\n")

        
