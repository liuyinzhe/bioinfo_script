from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re

fasta_file = "all.mas.fas"
seq_obj = SeqIO.parse(fasta_file, "fasta")

seq_list = []
for seq_record in seq_obj:
    print(seq_record.id)
    ref_seqence = str(seq_record.seq)
    
    seq_list.append(re.split("",ref_seqence))


new_seq = ""
index = 1
pos_list = []
start = 0
for tuple_obj in zip(*seq_list):
    #print(tuple_obj)
    rmdup = set(tuple_obj)
    #print(rmdup)
    if len(rmdup) == 1:
        
        base = list(rmdup)[0] 
        if base == "-":
            new_seq += "N"
            if index != start and index-start !=1:
                #print(start,index,index-start)
                pos_list.append([start,index,index-start])
            start=index+1
        else:
            new_seq += base
    else:
        new_seq += "N"
        if index != start and index-start !=1:
            #print(start,index,index-start)
            pos_list.append([start,index,index-start])
        start=index+1
    index +=1
new_id = 'consensus_N'
# 创建一个SeqRecord对象
record = SeqRecord(Seq(new_seq), id=new_id, description="")
 
# 写入FASTA文件
with open("consensus_N.fasta", "w") as file:
    SeqIO.write(record, file, "fasta")

for x in sorted(pos_list,key=lambda x:x[2],reverse=True):
    print(x)
