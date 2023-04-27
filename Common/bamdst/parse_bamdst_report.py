import re
import os
from pathlib import Path




def parse_bamdst_report(sample,report_file):
    '''
    '''
    # fastp 内容表头 
    summary_header = []
    sample_value_dic = {}
    sample_value_dic[sample] = []
    with open(report_file,mode='rt',encoding='utf-8') as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            new_line = re.split("\s{2,}",line.strip())[0]
            record = re.split("\t",new_line.strip())
            #print(record)
            name = record[0]
            summary_header.append(name)
            value = record[1]
            sample_value_dic[sample].append(value)
        #print(len(sample_value_dic[sample]))
    return summary_header,sample_value_dic


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
    file_list = GetAllFilePaths(pwd,wildcard='coverage.report')
    sample_name_list = []
    summary_header = []
    all_value_dic = {}
    for sample_path in file_list:
        # print(sample_path.name)  # 文件名
        # print(sample_path.parent) # 上级
        # print(sample_path.suffix) # 后缀
        # print(sample_path.parent.stem) # 主目录

        sample_name = sample_path.parent.stem
        sample_name_list.append(sample_name)
        summary_header,sample_value_dic = parse_bamdst_report(sample_name,sample_path)
        all_value_dic.update(sample_value_dic)
        #print(summary_header)


    with open('all.bamdst_report.tsv',mode='wt',encoding='utf-8') as out:
        out.write('row_name\t'+'\t'.join(sample_name_list)+'\n')

        for idx in range(len(summary_header)):
            out.write(summary_header[idx])
            for sample in sample_name_list:
                out.write('\t'+all_value_dic[sample][idx])
            out.write("\n")


if __name__ == '__main__':
    main()
