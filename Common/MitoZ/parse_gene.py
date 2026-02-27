import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
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
        if child.is_symlink():
            pass
        elif child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst


def main():
    current_dir = Path.cwd()
    file_paths = GetAllFilePaths(current_dir,wildcard='mitoz_*.gbf.gene.fasta')
    target_gene_lst = ["COX1","CYTB","ND4L"]
    target_info_dic = {} # 样品:{seq_id:seq}
    for gene_file in file_paths:
        sample_name = re.split(r"\.",gene_file.name)[0]
        sample_name = re.sub("mitoz_","",sample_name)
        #print(sample_name)
        seq_obj = SeqIO.parse(str(gene_file), "fasta")
        seq_dic = {}
        for record in seq_obj:
            #print(record.id)  #JFS26;trnH(gug);len=69;[10348:10417](+)
            info_lst= re.split(";",record.id)
            #print(info_lst)
            sample_name = info_lst[0]
            seq_id = info_lst[1]
            len_info = info_lst[2]
            gene_seq = str(record.seq)
            seq_len = len(gene_seq)
            pos_info = info_lst[3]
            if sample_name not in target_info_dic:
                target_info_dic[sample_name] = {}
            if seq_id in target_gene_lst:
                target_info_dic[sample_name][seq_id]  = [gene_seq,seq_len]
            # print(seq_id)
            # seq_dic[seq_id]=str(record.seq)
    #写入
    outdir = current_dir.joinpath("gene_stat")
    outdir.mkdir(parents=True,exist_ok=True)
    xls_file = outdir.joinpath("gene_len.xls")
    with open(xls_file,mode='wt',encoding="utf-8") as out:
        out.write("Sample\tGene_Name\tgene_len\n")
        for sample_name in target_info_dic:
            for gene_name in target_gene_lst:
                if gene_name not in target_info_dic[sample_name]:
                    out.write("\t".join([sample_name,gene_name,"False"])+"\n")
                    continue
                gene_seq,gene_len = target_info_dic[sample_name][gene_name]
                gene_fasta_path = outdir.joinpath(sample_name+"."+gene_name+".fasta")
                description_str = "length="+str(gene_len)
                record = SeqRecord(Seq(gene_seq), id=sample_name+"."+gene_name, description=description_str)
                SeqIO.write(record, gene_fasta_path, "fasta")
                out.write("\t".join([sample_name,gene_name,str(gene_len)])+"\n")


'''
    单独循环写
            description_str = ";".join(["len="+str(len(D_loop_seq)),str(d_loop_pos)])
            record = SeqRecord(Seq(D_loop_seq), id=sample_name+".D_loop", description=description_str)
            SeqIO.write(record, D_loop_path, "fasta")
'''
if __name__ == '__main__':
    main()
