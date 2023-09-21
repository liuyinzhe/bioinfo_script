import re
import os
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



def main():

    ## 跳转脚本所在目录
    pwd = os.path.split(os.path.realpath(__file__))[0]
    #pwd = os.getcwd()
    pwd = Path(pwd)
    os.chdir(pwd)
    file_list = GetAllFilePaths(pwd,wildcard='*.dna')
    #print(file_list)
    with open ("all.fasta",mode='wt',encoding='utf-8') as out:
        for sample_path in file_list:
            #print(type(sample_path))
            sample = re.split(r"\.",str(sample_path.name))[0]
            sample = re.sub("\s","_",sample)
            file_path = sample_path
            print(sample)
            print(file_path)
            # 读文件
            with open(file_path,mode='rb') as fh:
                line_first = fh.readline()
                line_str = str(line_first)
                #print(line_str)
                line=re.search(r'[atgcATGC]{10,}',line_str).group(0)
                print(line)
                #break
                out.write(">"+sample+"\n")
                out.write(line.strip()+"\n")
            #break

if __name__ == '__main__':
    main()
