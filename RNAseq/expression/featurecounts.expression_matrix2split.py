import re

all_sample_dic = {} # sample_name:[num,num,num]


# 计算key_list 数量长度,超出了就不添加
key_str_lst = []
with open("all.counts.txt",mode='rt',encoding='utf-8') as fh:
    sample_lst = []
    for line in fh:
        if line.startswith("#"):
            continue
        '''
        Geneid	Chr	Start	End	Strand	Length	A1.sorted.bam	A2.sorted.bam	A3.sorted.bam	A4.sorted.bam	B1.sorted.bam	B2.sorted.bam	B3.sorted.bam	B4.sorted.bam
        0        1    2      3     4      5       6-
        '''
        record = re.split("\t",line.strip())
        if line.startswith("Geneid"):
            sample_tmp_list = record[6:]
            for sample_tmp in sample_tmp_list:
                sample_name = re.sub(".sorted.bam","",sample_tmp)
                if sample_name not in sample_lst:
                    sample_lst.append(sample_name)
                if sample_name not in all_sample_dic:
                    all_sample_dic[sample_name] = []
            continue
        key_str = '\t'.join(record[0:6])
        key_str_lst.append(key_str)
        #print(key_str)
        # 
        for index in range(len(sample_lst)):
            sample_name = sample_lst[index]
            all_sample_dic[sample_name].append(record[6+index])

            
# # 读取第二个

# # 计算key_list 数量长度,超出了就不添加
# line_count = len(key_str_lst)
# with open("A_C.counts.txt",mode='rt',encoding='utf-8') as fh:
#     sample_lst = []
#     for line in fh:
#         if line.startswith("#"):
#             continue
#         '''
#         Geneid	Chr	Start	End	Strand	Length	A1.sorted.bam	A2.sorted.bam	A3.sorted.bam	A4.sorted.bam	B1.sorted.bam	B2.sorted.bam	B3.sorted.bam	B4.sorted.bam
#         0        1    2      3     4      5       6-
#         '''
#         record = re.split("\t",line.strip())
#         if line.startswith("Geneid"):
#             sample_tmp_list = record[6:]
#             for sample_tmp in sample_tmp_list:
#                 sample_name = re.sub(".sorted.bam","",sample_tmp)
#                 if sample_name not in sample_lst:
#                     sample_lst.append(sample_name)
#                 if sample_name not in all_sample_dic:
#                     all_sample_dic[sample_name] = []
#             continue
#         key_str = '\t'.join(record[0:6])
#         key_str_lst.append(key_str)
#         #print(key_str)
#         # 
#         for index in range(len(sample_lst)):
#             sample_name = sample_lst[index]
#             if len(all_sample_dic[sample_name]) == line_count:
#                 continue
#             all_sample_dic[sample_name].append(record[6+index])


# # 读取第3个
# with open("B_C.counts.txt",mode='rt',encoding='utf-8') as fh:
#     sample_lst = []
#     for line in fh:
#         if line.startswith("#"):
#             continue
#         '''
#         Geneid	Chr	Start	End	Strand	Length	A1.sorted.bam	A2.sorted.bam	A3.sorted.bam	A4.sorted.bam	B1.sorted.bam	B2.sorted.bam	B3.sorted.bam	B4.sorted.bam
#         0        1    2      3     4      5       6-
#         '''
#         record = re.split("\t",line.strip())
#         if line.startswith("Geneid"):
#             sample_tmp_list = record[6:]
#             for sample_tmp in sample_tmp_list:
#                 sample_name = re.sub(".sorted.bam","",sample_tmp)
#                 if sample_name not in sample_lst:
#                     sample_lst.append(sample_name)
#                 if sample_name not in all_sample_dic:
#                     all_sample_dic[sample_name] = []
#             continue
#         #print(key_str)
#         key_str = '\t'.join(record[0:6])
#         key_str_lst.append(key_str)
#         # 
#         for index in range(len(sample_lst)):
#             sample_name = sample_lst[index]
#             if len(all_sample_dic[sample_name]) == line_count:
#                 continue
#             all_sample_dic[sample_name].append(record[6+index])

print(all_sample_dic.keys())

sample_group_lst = [
    ['B1','B2','B3','C1','C2','C3', ], # B vs C
    ['H1','H2','H3','C1','C2','C3', ], # H vs C
]
file_name_lst = ['B_vs_C','H_vs_C']

header_part="Geneid\tChr\tStart\tEnd\tStrand\tLength"
for index in range(len(sample_group_lst)):
    target_name_lst = sample_group_lst[index]
    file_name = "all."+file_name_lst[index]+".counts.txt"
    with open(file_name,mode="wt",encoding='utf-8') as out:
        out.write(header_part+'\t'+'\t'.join(target_name_lst)+'\n')
        for key_idx in range(len(key_str_lst)):
            key_str = key_str_lst[key_idx]
            out.write(key_str)
            for sample_name in target_name_lst:
                value_str = all_sample_dic[sample_name][key_idx]
                out.write('\t'+value_str)
            out.write('\n')

            

        
