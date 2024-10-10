from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re

# V H D B 
IUPAC_dic = {
    'M' : ['A','C'],
    'R' : ['A','G'],
    'W' : ['A','T'],
    'S' : ['C','G'],
    'Y' : ['C','T'],
    'K' : ['G','T']
}

'''
# https://qinqianshan.com/biology/genetalks/iupac-ambiguity-codes/
IUPAC Code		Meaning		Complement
A				A				T
C				C				G
G				G				C
T/U				T				A
M				A or C			K
R				A or G			Y
W				A or T			W
S				C or G			S
Y				C or T			R
K				G or T			M
V				A or C or G		B
H				A or C or T		D
D				A or G or T		H
B				C or G or T		V
N			G or A or T or C	N
'''
fasta_file = "ref.fa"
seq_obj = SeqIO.parse(fasta_file, "fasta")


ref_seqence = ""
for seq_record in seq_obj:
    #print(seq_record.id)
    ref_seqence = seq_record.seq

new_seq = ""
for seq_record in SeqIO.parse("TZ84-01M-2308001.assembly_based.with_ambiguity_codes.fa", "fasta"):
    #print(seq_record.id)
    new_seq = seq_record.seq
#print(len(ref_seqence),len(new_seq))


# 判断是否有  V H D B  N
match_list = re.findall("[VHDBN]",str(new_seq),flags=re.IGNORECASE)
#print(match_list)
if len(match_list) >0:
    print("有VHDBN碱基存在,脚本不适合")
#print(ref_seqence[0:4])
revised_seq = ""
for i in range(len(ref_seqence)):
    ref_base_char = ref_seqence[i]
    new_base_char = new_seq[i]
    if ref_base_char != new_base_char:
        Ambiguity_Codes = IUPAC_dic[new_base_char]
        # 异或
        index =Ambiguity_Codes.index(ref_base_char) ^ 1
        # print(ref_base_char,new_base_char,Ambiguity_Codes,index)
        revised_seq += Ambiguity_Codes[index]
    else:
        revised_seq += ref_base_char

new_id = 'Assembly_based'
# 创建一个SeqRecord对象
record = SeqRecord(Seq(revised_seq), id=new_id, description="")
 
# 写入FASTA文件
with open("TZ84-01M-2308001.replace_ambiguity_codes.fasta", "w") as file:
    SeqIO.write(record, file, "fasta")


# biopython读取fasta文件
# https://blog.51cto.com/u_16175453/7878003
