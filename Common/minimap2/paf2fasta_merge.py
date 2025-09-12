from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re
import shutil
from pathlib import Path

def reverse_complement(seq):
    '''get reverse complement  seq'''
    rule = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N',']':'[', '[':']'}
    return ''.join([rule[each] for each in seq.upper()][::-1])

def reverse_seq(seq):
    '''get reverse complement  seq'''
    rule = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N',']':'[', '[':']'}
    return ''.join([each for each in seq.upper()][::-1])

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
        if child.is_symlink():
            pass
        elif child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child) #Path object
    return files_lst

def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()

    # 存储所有序列ID 与序列
    seq_dic = {}
    for record in SeqIO.parse("assembly.fasta", "fasta"):
        # 更新描述信息
        seq_id = record.id
        seq_base = record.seq
        seq_dic[seq_id] = seq_base.strip()

    # 读取PAF 获取 序列id  坐标，以及长度 方向
    paf_lst = []
    with open("aln.paf",mode='rt',encoding='utf-8') as fh:
        for line in fh:
            record = re.split("\t",line.strip())
            # 2	10598	5202	5662	-	insert	6620	4026	4486	460	460	60	NM:i:0	ms:i:460	AS:i:460	nn:i:0	tp:A:P	cm:i:48	s1:i:445	s2:i:0	de:f:0	rl:i:0	cg:Z:460M
            # 5	2549	0	2227	+	insert	6620	4393	6620	2227	2227	60	NM:i:0	ms:i:2227	AS:i:2227	nn:i:0	tp:A:P	cm:i:211	s1:i:2204	s2:i:48	de:f:0	rl:i:0	cg:Z:2227M
            query_seq_name,query_seq_len,query_start,query_end,stand,target_seq_name,target_seq_len,target_start,target_end,residue_match,aln_block_len,map_quality = record[0:12]
            paf_lst.append([query_seq_name,int(query_start),int(query_end),stand,target_seq_name,int(target_start),int(target_end)])
                           #  0               1           2        3        4              5             6

    sorted_paf_lst = sorted(paf_lst,key=lambda x:[x[5],x[6]])
    
    #print(sorted_paf_lst)

    with open("codes.fasta", "w") as file:
        all_seq = ""
        last_start = 0
        last_end = 0
        last_base = ""
        first_flag = True
        for paf in sorted_paf_lst:
            overlap_falg = False
            #query_seq_name,query_start,query_end,stand,target_seq_name,target_start,target_end= paf
            query_seq_name,query_start,query_end,stand,target_seq_name,target_start,target_end= paf
            seq_bases = seq_dic[query_seq_name]
            print(stand)
            # print(target_start,target_end)
            diff_offset = 0 # overlap 则设置偏移
            if last_end > target_start and target_end <= last_end: # 存在完全覆盖,跳过
                '''
                6       2485
                6       164
                '''
                continue
            elif  last_end > target_start: # 部分覆盖
                overlap_falg = True
                '''
                6       2485
                2465       2495
                '''
                # 计算overlap 偏移
                diff_offset = last_end - target_start
            if query_start + diff_offset > query_end: # 如果偏移累加后超过了 end 跳过
                continue

            if stand == "+": # 根据序列方向,提取具体序列，后面方便按照提供的参考拼接
                seq_bases = seq_dic[query_seq_name][query_start:query_end]#reverse_complement(seq_dic[query_seq_name])
            else:
                seq_bases = reverse_complement(seq_dic[query_seq_name][query_start:query_end]) #reverse_complement(seq_dic[query_seq_name]) #reverse_seq(seq_dic[seq_id])
            
            if  overlap_falg :
                print("last",last_start,last_end)
                print("target",target_start,target_end)
                print("diff_offset",diff_offset)
                # print(reverse_complement(seq_dic["2"][5202:5662])[-93:])
                # print(seq_dic["5"][0:2227][0:93])
                # print(last_base[-93:])
                # print(seq_bases[0:93]) # 重叠的93bp,保留上一个 不填写N 直接连接
                seq_bases = seq_bases[0:diff_offset]
            '''
            2  4026    4486
            5  4393    6620
            '''
            if overlap_falg :
                all_seq += seq_bases #+ "N" # 直接连接
            elif first_flag:
                all_seq += seq_bases
                first_flag = False
            else:
                all_seq += seq_bases + "N"  # 末尾追加N
                
            last_start = target_start
            last_end = target_end
            last_base = seq_bases
            
        record = SeqRecord(Seq(all_seq[:-1]), id="scaffold", description="")
        SeqIO.write(record, file, "fasta")

if __name__ == "__main__":
    main()