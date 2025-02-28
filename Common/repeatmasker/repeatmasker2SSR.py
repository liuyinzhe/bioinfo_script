import pandas as  pd
from pathlib import Path
import re
from collections import OrderedDict

def is_overlap(region_a, region_b):
    """
    :param region_a: List[int,int]
    :param region_b: List[int,int]
    :return: Bool
    """
    return max(region_a[0], region_b[0]) <= min(region_a[1], region_b[1])

def main():
    script_path =Path(__file__)
    scripts_dir = Path(script_path).parent
    current_dir = Path.cwd()

    excel_df = pd.read_excel("RM_vs_SM.merge_result_info.xlsx")
    #print(excel_df)
    '''
    gene_id	chromosome	start	end	description
    '''
    gene_pos_dic = OrderedDict()
    # 存储基因名和坐标信息
    for index,row in excel_df.iterrows():
        gene_id = row['gene_id']
        chromosome = row['chromosome']
        start = row['start']
        end = row['end']
        description = row['description']
        gene_pos_dic[gene_id] = [chromosome,start,end,description]
    

    # 解析chr4.fa.out 文件
    out_list = []
    with open("chr4.fa.out",mode='rt',encoding ='utf-8') as fh:
        '''
            SW   perc perc perc  query     position in query              matching      repeat           position in repeat
        score   div. del. ins.  sequence  begin    end          (left)   repeat        class/family   begin  end    (left)    ID

            17   28.0  0.0  1.7  chr4          1197     1255 (29771989) + (ATAACG)n     Simple_repeat       1     58    (0)     1 
            0     1     2    3     4            5          5     7      8     9            10               11    12    13     14
        '''
        for line in fh:
            if line.startswith("   SW"):
                continue
            elif line.startswith("score   div. del. ins."):
                continue
            if  not line.strip():
                continue
            record = re.split("\s+",line.strip())
            #print(record)
            chrom = record[4]
            start = int(record[5])
            end = int(record[6])
            repeat_unin = record[9]

            repeat_type = record[10]
            #print([chrom,start,end,report_type,repeat_unin])
            if repeat_type != "Simple_repeat":
                continue
            new_repeat_unin = re.sub("[\(\)n]","",repeat_unin)
            if len(set(new_repeat_unin))<2:
                continue
            repeat_unin_len = len(new_repeat_unin)
            repeat_seq_len = end-start
            repeat_times = repeat_seq_len/len(new_repeat_unin)
            if repeat_unin_len >6: # 2-6
                continue
            elif repeat_times<5:
                continue
            pos_info = chrom+":"+str(start)+"-"+str(end) # chr2:105472100-105472101
            #print(repeat_unin,repeat_unin_len,repeat_times,repeat_seq_len)
            if start >=25121479 and end<=29757504:
                out_list.append([pos_info,chrom,start,end,repeat_unin,repeat_unin_len,repeat_times,repeat_seq_len])
    out_dic = {
        "染色体位置":[],
        "基因和转录本":[],
        "重复单元":[],
        "重复次数":[],
        "SSR长度":[],
    }
    # 遍历添加基因名信息
    for info in out_list:
        pos_info,chrom,start,end,repeat_unin,repeat_unin_len,repeat_times,repeat_seq_len = info
        for gene_id,value in gene_pos_dic.items():#chromosome,start,end,description
            chromosome,g_start,g_end,description = value
            if is_overlap([start,end+1],[g_start,g_end]):
                out_dic["染色体位置"].append(pos_info)
                out_dic["基因和转录本"].append(gene_id)

                out_dic["重复单元"].append(repeat_unin)
                out_dic["重复次数"].append(repeat_times)
                out_dic["SSR长度"].append(repeat_seq_len)
                break
        if pos_info not in out_dic["染色体位置"]:
            out_dic["染色体位置"].append(pos_info)
            out_dic["基因和转录本"].append("unknown")

            out_dic["重复单元"].append(repeat_unin)
            out_dic["重复次数"].append(repeat_times)
            out_dic["SSR长度"].append(repeat_seq_len)

    #print(out_dic)
    out_df = pd.DataFrame(out_dic)
    out_df.to_excel("测试.xlsx",index=False)
    # 50 侧翼
    #complete_seq = genome[chrom][start-flank_size:end+1+flank_size].seq
    out_50_dic = {
        "染色体位置":[],
        "基因和转录本":[],
        "重复单元":[],
        "重复次数":[],
        "SSR长度":[],
    }
    flank_size = 50
    # 遍历添加基因名信息
    for info in out_list:
        pos_info,chrom,start,end,repeat_unin,repeat_unin_len,repeat_times,repeat_seq_len = info
        for gene_id,value in gene_pos_dic.items():#chromosome,start,end,description
            chromosome,g_start,g_end,description = value
            if is_overlap([start-flank_size,end+1+flank_size],[g_start,g_end]):
                out_50_dic["染色体位置"].append(pos_info)
                out_50_dic["基因和转录本"].append(gene_id)

                out_50_dic["重复单元"].append(repeat_unin)
                out_50_dic["重复次数"].append(repeat_times)
                out_50_dic["SSR长度"].append(repeat_seq_len)
                break
        if pos_info not in out_50_dic["染色体位置"]:
            out_50_dic["染色体位置"].append(pos_info)
            out_50_dic["基因和转录本"].append("unknown")

            out_50_dic["重复单元"].append(repeat_unin)
            out_50_dic["重复次数"].append(repeat_times)
            out_50_dic["SSR长度"].append(repeat_seq_len)
    #print(out_50_dic)
    out_50_df = pd.DataFrame(out_50_dic)
    out_50_df.to_excel("测试.flk50.xlsx",index=False)
if __name__ == '__main__':
    main()
