
from pathlib import Path
import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


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



def modify_fasta(sample_name,topology,read_fasta_path,save_fasta_path):
    
    seq_obj = SeqIO.parse(read_fasta_path, "fasta")
    modified_records = []
    for record in seq_obj:
        # 'topology=linear' or 'topology=circular'
        # record.id = record.id
        record.id = sample_name + " " + topology
        # 清除 description
        record.description = ""
        # 创建一个SeqRecord对象
        # new_id = record.id + "#"
        # new_seq = str(record.seq)
        #record = SeqRecord(Seq(new_seq), id=new_id, description="")
        modified_records.append(record)

    with open(save_fasta_path, mode="w",encoding="utf-8") as output_handle:
        SeqIO.write(modified_records, output_handle, "fasta")
    return


def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()

    # animal_mt.K125.scaffolds.graph1.1.path_sequence.fasta
    # animal_mt.K127.complete.graph1.1.path_sequence.fasta
    file_paths = GetAllFilePaths(current_dir,wildcard="*.path_sequence.fasta")
    save_dir = current_dir.joinpath("mitoz_input_fasta")
    save_dir.mkdir(parents=True,exist_ok=True)

    for fasta_file in file_paths:

        file_name = fasta_file.name
        sample_name = fasta_file.parent.name
        if "complete" in file_name:
            topology = "circular"
            part_name = "complete"
        else:
            topology = "linear"
            part_name = "scaffolds"
        fasta_name = ".".join([sample_name,part_name,"fasta"])
        fasta_save_path = save_dir.joinpath(fasta_name)
        modify_fasta(sample_name,topology,str(fasta_file),fasta_save_path)
    '''
    读取文件,根据文件名修改序列名字
    重新写到特定目录
    '''
    


if __name__ == "__main__":
    main()

