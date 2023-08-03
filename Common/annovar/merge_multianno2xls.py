import json
import re
import os
from pathlib import Path
import math



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

def get_info(input_file,sample_name_lst,index,result_dic):
    sample_len = len(sample_name_lst)
    with open(input_file,mode='rt', encoding='utf-8') as fh:
        for line in fh:
            #if line.startswith("Chr"):
            #    continue
            record = re.split('\t',line.strip())
            
            if 'Func.refGene' in line:
                header_lst = record[0:-13]
                continue
            # 存储 作为key
            key = '\t'.join(record[0:-13]+[record[-2],])
            #print(key)
            if key not in result_dic:
                result_dic[key] = ['.']*sample_len
                result_dic[key][index] = record[-1]
            else:
                # print(index)
                # print(record)
                # print(len(record))
                # print(result_dic[key])
                result_dic[key][index] = record[-1]
    return result_dic

def main():

    ## 跳转脚本所在目录
    pwd = os.path.split(os.path.realpath(__file__))[0]
    #pwd = os.getcwd()
    pwd = Path(pwd)
    os.chdir(pwd)
    file_list = GetAllFilePaths(pwd,wildcard='*.hg38_multianno.txt')
    sample_dic = {}
    sample_name_lst = []
    index = 0
    for sample_path in file_list:
        #print(type(sample_path))
        sample = re.split(r"\.",str(sample_path.name))[0]
        #print(sample)
        sample_name_lst.append(sample)# 样品名
        sample_dic[sample] = index
        index += 1

    header_lst = []
    print(file_list[0])
    with open(file_list[0],mode='rt', encoding='utf-8') as fh:
        for line in fh:
            record = re.split('\t',line.strip())
            if 'Func.refGene' in line:
                header_lst = record[0:-13]
                header_lst.append('FORMAT')# record[-2] # GT:AD:DP:GQ:PL
    print(header_lst)

    # 
    header_lst = header_lst + sample_name_lst
    header_str = '\t'.join(header_lst)


    result_dic = {} # 全局
    for sample_path in file_list:
        #print(type(sample_path))
        sample = re.split(r"\.",str(sample_path.name))[0]
        # 读文件存字典 [sample_name_lst],全部存储
        index = sample_dic[sample]
        result_dic = get_info(sample_path,sample_name_lst,index,result_dic)

    # 排序
    with open('all.summary.tsv',mode='wt',encoding='utf-8') as out:
        out.write(header_str+'\n')
        # sorted(result_dic.items(),key = lambda x:x[1],reverse = True)
        #key_list = sorted(result_dic.keys(),key = lambda x:(sum(map(ord,re.sub('chr','',re.split('\t',x)[0]))),int(re.split('\t',x)[1])),reverse = False)
        #key_list = sorted(result_dic.keys(),key = lambda x:(re.sub('chr','',re.split('\t',x)[0]),int(re.split('\t',x)[1])),reverse = False)
        key_list = sorted(result_dic.keys(),key = lambda x:(re.sub('chr','',re.split('\t',x)[0]),int(re.split('\t',x)[1])),reverse = False)
        for key in key_list:
            #print(re.split('\t',key)[0])
            #print(re.split('\t',key)[1])
            #print(re.split('\t',key)[2])
            out.write(key+'\t'+'\t'.join(result_dic[key])+'\n')


if __name__ == '__main__':
    main()

