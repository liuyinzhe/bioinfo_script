import re
import argparse
import sys
from pathlib import Path

def get_args():
    '''
    python stat.py -i result.xls
    '''
    parser = argparse.ArgumentParser(
        description='''''', usage="python3 %(prog)s [options]")
    # 输入文件
    parser.add_argument(
        "-i","--input_path", help="Path of table tsv.", required=True,type=str, metavar="File")
    # group
    parser.add_argument(
        "-m","--meta_path", help="Path of meta tsv.", required=True,type=str, metavar="File")
    # 输出目录
    parser.add_argument(
        "-o","--outdir", help="The directory of the result output;default: current working directory.",
        default=Path.cwd(), metavar="DIR")
    
    # 输出文件与输入文件路径相同
    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()

    return args

def parse_meta_info(meta_path):
    '''

    #SampleID       Treatment
    #q2:types       categorical
    S12     HH
    S13     HH
    S14     HH
    M31     Normal
    M32     Normal
    M41     Normal

    '''
    sample2group_dic = {}
    with open(meta_path,mode='rt',encoding='utf-8') as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            record = re.split("\t",line.strip()) #sample group
            sample = record[0]
            group = record[1]
            
            if sample not in sample2group_dic:
                sample2group_dic[sample] = group
            else:
                print("Warring:repeat sample:{}!".format(sample))
                exit(1)
    return sample2group_dic

def main():
    '''
    (0) level 输出到7
    (1) 第6个是__ 的去掉 __ ,保留到上一级别，保留; ";s__" 去掉
    d__Bacteria;__;__;__;__;__
    Unassigned;__;__;__;__;__
    (2) ; 替换为 |
    (3) 第一行 class 分组内容 第二行 ID
    (4) g__uncultured 、Constructed 过滤掉
    (5) s/taxonomy//g; 将标题行中的 taxonomy 一词删除


    16S V3 V4 区域查看是否可以区分
    拉丁名,物种序列
    '''
    args = get_args()
    input_tsv = Path(args.input_path)
    #collapse.frequency.table.tsv
    #collapse.frequency.table.lefse.tsv
    outdir = Path(args.outdir)
    meta_path = args.meta_path
    sample2group_dic = parse_meta_info(meta_path)
    file_name = re.sub(".tsv$",".lefse.tsv",input_tsv.name)
    out_path = outdir.joinpath(file_name)
    #
    with open(input_tsv,mode='rt',encoding="utf-8") as fh,\
        open(out_path,mode='wt',encoding="utf-8") as out:
        for line in fh:
            if line.startswith("# Constructed from biom file"):
                continue
            if line.startswith("#OTU ID"):
                new_line = re.sub("\ttaxonomy","",line.strip())
                new_line = re.sub("#OTU ID","ID",new_line)
                sample_list = re.split("\t",new_line)[1:]
                group_list = [sample2group_dic[x] for x in sample_list]
                sample_list.insert(0,'ID')
                group_list.insert(0,'class')
                out.write("\t".join(group_list)+"\n")
                out.write("\t".join(sample_list)+"\n")
                continue
            record = re.split("\t",line.strip())
            last_name = re.split("\t",record[0])[-1]
            if last_name == "Constructed":
                continue
            new_ID = re.sub(";__","",record[0]) # 删除多余内容
            new_ID = re.sub(";s__$","",new_ID) 
            new_ID = re.sub("g__uncultured$","",new_ID)
            new_ID = re.sub("f__uncultured$","",new_ID)
            record[0] = re.sub(r";",r"|",new_ID) # 替换分割符号
            out.write("\t".join(record)+"\n")





if __name__ == '__main__':
    main()