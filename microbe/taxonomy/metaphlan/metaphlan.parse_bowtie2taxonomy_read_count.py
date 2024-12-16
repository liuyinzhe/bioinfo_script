import bz2
import re
from pathlib import Path
import pandas as pd
from collections  import Counter
def GetAllFilePaths(pwd,wildcard='*'):
    '''
    获取目录下文件全路径，通配符检索特定文件名，返回列表
    param: str  "pwd"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    target_path=Path(pwd)
    for child in target_path.rglob(wildcard):
        if child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst


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
                taxonomy_info = taxonomy_info
                taxonomy_lst.append(taxonomy_info)
            else:
                print("Warring!：not match:\t\""+records[index]+"\"\n")
                continue
                #taxonomy_lst.append('NA')
        else: # 超出范围
            continue
            #taxonomy_lst.append('NA')
    return taxonomy_lst

def read_bowtie2(bowtie2_file):
    sample_mark_list = []
    with bz2.open(bowtie2_file,mode='rt',encoding='utf-8') as fh:
        for line in fh:
            #print(line.strip())
            '''
            LH00708:25:22JFV3LT4:2:1124:9691:3045:N:0:GCATAACG+CAAGAAGC#0/1 610243__A0A060QJF7__ASAP_2763
            LH00708:25:22JFV3LT4:2:1124:27195:14518:N:0:GCATAACG+CAAGAAGC#0/1       610243__A0A060QJF7__ASAP_2763
            LH00708:25:22JFV3LT4:2:1124:8906:19420:N:0:GCATAACG+CAAGAAGC#0/1        610243__A0A060QJF7__ASAP_2763
            '''
            if line.startswith("#"):
                continue
            read_name,mark_id = re.split("\t",line.strip())
            mark_id = re.split(":",mark_id)[-1]
            sample_mark_list.append(mark_id)
    return sample_mark_list

# 读取mark 获得字典
def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    # print(script_dir)
    current_dir = Path.cwd()

    mark_id_dic = {}
    taxonomy_type = ['kingdom','phylum','class','order','family','genus','species']
    marker_info = "/data/home/qinhongshuang/.conda/envs/mpa/lib/python3.7/site-packages/metaphlan/metaphlan_databases/mpa_v30_CHOCOPhlAn_201901_marker_info.txt"
    with open(marker_info,mode='rt',encoding='utf-8') as fh:
        for line in fh:
            mark_id,info_str = re.split("\t",line.strip())
            '''
            'taxon': 'k__Viruses|p__Viruses_unclassified|c__Viruses_unclassified|o__Viruses_unclassified|f__Iridoviridae|g__Lymphocystivirus|s__Lymphocystis_disease_virus_isolate_China'
            k__Bacteria|p__Proteobacteria|c__Alphaproteobacteria|o__Rhodobacterales|f__Hyphomonadaceae|g__Henriciella|s__Henriciella_barbarensis
            '''
            '''
            244590__GeneID:2658371	{'ext': [], 'score': 0.0, 'clade': 's__Sulfolobus_spindle_shaped_virus_2', 'len': 147, 'taxon': 'k__Viruses|p__Viruses_unclassified|c__Viruses_unclassified|o__Viruses_unclassified|f__Fuselloviridae|g__Alphafusellovirus|s__Sulfolobus_spindle_shaped_virus_2'}

            {'clade': 's__Meiothermus_hypogaeus', 'score': 0, 'ext': ['GCA_003568585'], 'len': 1080, 'taxon': 'k__Bacteria|p__Deinococcus-Thermus|c__Deinococci|o__Thermales|f__Thermaceae|g__Meiothermus|s__Meiothermus_hypogaeus'}
            
            未能匹配 {'clade': 's__Meiothermus_hypogaeus', 'score': 0, 'ext': ['GCA_000376665', 'GCA_000024425', 'GCA_000346125', 'GCA_000836395'], 'len': 354, 'taxon': 'k__Bacteria|p__Deinococcus-Thermus|c__Deinococci|o__Thermales|f__Thermaceae|g__Meiothermus|s__Meiothermus_hypogaeus'}
未能匹配 {'clade': 's__Meiothermus_hypogaeus', 'score': 0, 'ext': ['GCA_000376665', 'GCA_000024425', 'GCA_000346125', 'GCA_000836395'], 'len': 198, 'taxon': 'k__Bacteria|p__Deinococcus-Thermus|c__Deinococci|o__Thermales|f__Thermaceae|g__Meiothermus|s__Meiothermus_hypogaeus'}
未能匹配 {'clade': 's__Meiothermus_hypogaeus', 'score': 0, 'ext': ['GCA_000376665', 'GCA_000024425', 'GCA_000346125', 'GCA_000836395'], 'len': 552, 'taxon': 'k__Bacteria|p__Deinococcus-Thermus|c__Deinococci|o__Thermales|f__Thermaceae|g__Meiothermus|s__Meiothermus_hypogaeus'}
            '''
            info_dic = eval(info_str)
            taxonomy_str = info_dic['taxon']
            mark_id = re.split(":",mark_id)[-1]
            if  mark_id not in mark_id_dic:
                mark_id_dic[mark_id] = taxonomy_str
            else:
                print("重复的mark_id",mark_id)

            # match_compile = re.compile("\'taxon\': \'([\w|]+)\'")
            # match_obj = re.search(match_compile,info_str)
            # if match_obj:
            #     #print(match_obj.group(1))
            #     taxonomy_str = match_obj.group(1)
            #     mark_id_dic[mark_id] = taxonomy_str
            #     #taxonomy_lst = parse_taxonomy(taxonomy_str)
            # else:
            #     print("未能匹配",info_str)

    # 
    files_lst = GetAllFilePaths(current_dir,wildcard='*.bz2')
    sample2count_dic = {}
    sample_lst = []
    for bowtie2_file in files_lst:
        sample_name = re.split(r"\.",bowtie2_file.name)[0]
        sample_mark_list = read_bowtie2(bowtie2_file)
        sample_taxonomy_list = [mark_id_dic[mark_id] for mark_id in sample_mark_list]
        taxonomy_count_dic = dict(Counter(sample_taxonomy_list))
        if sample_name not in sample2count_dic:
            sample_lst.append(sample_name)
            sample2count_dic[sample_name] = taxonomy_count_dic
        else:
            print("重复的样品名",sample_name,bowtie2_file.name)
    
    taxonomy_type = ['kingdom','phylum','class','order','family','genus','species',"read_count"]
    # 生成数据框
    dataframe_dic_list = []

    for sample_name in sample_lst:
        taxonomy_count_dic = sample2count_dic[sample_name]
        # 单个样品的字典
        sample_dic = {
            'kingdom':[],
            'phylum':[],
            'class':[],
            'order':[],
            'family':[],
            'genus':[],
            'species':[],
            "read_count":[]
        }
        for taxonomy_str,count in taxonomy_count_dic.items():
            info_list = parse_taxonomy(taxonomy_str)
            kingdom,phylum,class_str,order,family,genus,species = info_list
            sample_dic['kingdom'].append(kingdom)
            sample_dic['phylum'].append(phylum)
            sample_dic['class'].append(class_str)
            sample_dic['order'].append(order)
            sample_dic['family'].append(family)
            sample_dic['genus'].append(genus)
            sample_dic['species'].append(species)
            sample_dic['read_count'].append(count)
        # dataframe_dic_list # sample_lst 中的顺序
        dataframe_dic_list.append(sample_dic)

    out_excel = current_dir.joinpath("taxonomy_read_count.xlsx")
    with pd.ExcelWriter(out_excel, engine='openpyxl', mode='w') as writer:
        for index in range(len(sample_lst)):
            sample_name = sample_lst[index]
            sample_dic = dataframe_dic_list[index]
            sample_df = pd.DataFrame.from_dict(sample_dic)
            sample_df.to_excel(writer, sheet_name=sample_name, index=False)

if __name__ == '__main__':
    main()

