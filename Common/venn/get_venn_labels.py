import re
import os
from pathlib  import Path
import pandas as pd

from itertools import chain
from pathlib import Path


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


def get_labels(data, fill=["number"]):
    # https://github.com/tctianchi/pyvenn/blob/master/venn.py
    """
    get a dict of labels for groups in data

    @type data: list[Iterable]
    @rtype: dict[str, str]

    input
      data: data to get label for
      fill: ["number"|"logic"|"percent"]

    return
      labels: a dict of labels for different sets

    example:
    In [12]: get_labels([range(10), range(5,15), range(3,8)], fill=["number"])
    Out[12]:
    {'001': '0',
     '010': '5',
     '011': '0',
     '100': '3',
     '101': '2',
     '110': '2',
     '111': '3'}
    """

    N = len(data)

    sets_data = [set(data[i]) for i in range(N)]  # sets for separate groups
    s_all = set(chain(*data))                     # union of all sets

    # bin(3) --> '0b11', so bin(3).split('0b')[-1] will remove "0b"
    set_collections = {}
    for n in range(1, 2**N):
        key = bin(n).split('0b')[-1].zfill(N)
        value = s_all
        sets_for_intersection = [sets_data[i] for i in range(N) if  key[i] == '1']
        sets_for_difference = [sets_data[i] for i in range(N) if  key[i] == '0']
        for s in sets_for_intersection:
            #print(s)
            value = value & s
        for s in sets_for_difference:
            value = value - s
        set_collections[key] = value
    # print(set_collections)
    labels = {k: "" for k in set_collections}
    if "logic" in fill:
        for k in set_collections:
            labels[k] = k + ": "
    if "number" in fill:
        for k in set_collections:
            labels[k] += str(len(set_collections[k]))
    if "percent" in fill:
        data_size = len(s_all)
        for k in set_collections:
            labels[k] += "(%.1f%%)" % (100.0 * len(set_collections[k]) / data_size)

    return labels,set_collections


def str_number2name(str_number,sample_name_order):
    '''
    0011
    00CD
    '''
    numbers = list(map(int,(list(str_number))))
    names = []
    for idx in range(len(numbers)):
        if numbers[idx] == 0:
            names.append("")
        else:
            names.append(sample_name_order[idx])

    return names




def main():
    # sample_name_order = ['set1','set2','set3','set4']
    # set1 = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"}
    # set2 = {"A", "B", "C", "D", "K", "L", "M", "N", "O", "P"}
    # set3 = {"A", "B", "C", "Q", "R", "S", "T", "U", "V", "W"}
    # set4 = {"A", "X", "Y", "Z"}
    # data_lst = []
    # data_lst.append(set1)
    # data_lst.append(set2)
    # data_lst.append(set3)
    # data_lst.append(set4)

    # labels,set_collections = get_labels(data_lst, fill=['number', 'logic'])
    # print(labels)
    # for k in set_collections:
    #     code_name = k
    #     set_name_list =str_number2name(code_name,sample_name_order)
    #     gene_id_list = list(set_collections[k])
    #     print(code_name,set_name_list,gene_id_list)
    # exit()

    
    pwd = Path.cwd()
    data_path = pwd.joinpath("data")
    gene_name_id_dict = {}
    sample_name_order = []
    data_lst = []
    files_lst = GetAllFilePaths(data_path,wildcard='*.xls')
    #print(len(files_lst))
    for index in range(len(files_lst)):
        file = files_lst[index]
        file_name = re.split("\.",str(file.name))[0]
        sample_name_order.append(file_name)
        excel_df = pd.read_csv(file,sep='\t',index_col=None)
        filter_df = excel_df[excel_df['Significant']=='yes']
        # 过滤后用于后续分析的gene id,主要为了保证基因id唯一，没有使用GeneName
        gene_id_filter_list = filter_df['Gene'].to_list()
        # 用于对应全部基因名
        gene_id_list = excel_df['Gene'].to_list()
        gene_name_list = excel_df['GeneName'].to_list()


        # dict(list(zip(*(two_lst))))  转字典
        tmp_dic = dict(list(zip(gene_id_list,gene_name_list)))
        gene_name_id_dict.update(tmp_dic)
        # 存储
        data_lst.append(set(gene_id_filter_list))
        
    labels,set_collections = get_labels(data_lst, fill=['number', 'logic'])
    #print(gene_name_id_dict)
    #print(sample_name_order)

    # print(len(labels))
    # print(len(set_collections))

    with open("venn_gene_info.xls",mode='wt',encoding='utf-8') as out:
        out.write('\t'.join(['code_name','gene_count','gene_id','gene_name','set1','set2','set3','set4'])+'\n')
        for k in set_collections:
            code_name = k
            #print("#",code_name)
            #print(str_number2name(code_name,sample_name_order))
            #print(type(k))
            gene_count = re.split(": ",labels[k])[1]
            gene_id_list = list(set_collections[k])
            #gene_name_list = [gene_name_id_dict[gene_id] for gene_id in gene_id_list]
            
            set_name_list =str_number2name(code_name,sample_name_order)
            for idx in range(len(gene_id_list)):
                gene_id = gene_id_list[idx]
                gene_name = gene_name_id_dict[gene_id]
                #print(code_name,gene_count,gene_id,gene_name)
                out_lst = ["'"+code_name,gene_count,gene_id,gene_name] + set_name_list
                #print(out_lst)
                out.write('\t'.join(out_lst)+'\n')

            
    target_gene_df = pd.read_excel("04 3d + 04 es 3d vs 05 3d + 05 es 3d 重叠基因 inflammatory.xlsx")
    target_gene_lst = target_gene_df['GeneName'].to_list()

    venn_gene_df = pd.read_csv('venn_gene_info.xls',encoding="utf-8",sep='\t',index_col=None)
    venn_gene_filter_df = venn_gene_df[venn_gene_df['gene_name'].isin(target_gene_lst)]
    
    venn_gene_filter_df.to_csv('venn_gene_info_filter.xls',encoding="utf-8",sep='\t',index=False)

    #GeneName

if __name__ == '__main__':
    main()
