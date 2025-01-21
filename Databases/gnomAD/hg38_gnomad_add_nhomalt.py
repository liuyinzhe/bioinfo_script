import pandas as pd
import pickle
from pathlib import Path
import gzip
import re
def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()
    # gnomad_nhomalt_dic # keys:value = "\t".join([chrom,start,stop,ref,alt]):nhomalt
    # database_path = Path("/data/database/gnomAD/Genomes_table/gnomad_nhomalt_dic.pkl")
    gzip_database_path = Path("/data/database/gnomAD/Genomes_table/gnomad_nhomalt_dic.pkl.gz")
    with gzip.open(gzip_database_path,mode='rb') as plk:
        gnomad_nhomalt_dic = pickle.load(plk)
    #gnomad_nhomalt_dic = pickle.load(open(database_path, 'rb'))
    gnomad_path =current_dir.joinpath("hg38_gnomad41_genome.txt")
    gnomad_nhomalt_path = current_dir.joinpath("hg38_gnomad41_genome_nhomalt.txt")
    with open(gnomad_path,mode='rt') as fh,\
        open(gnomad_nhomalt_path,mode='wt') as out:
        for line in fh:
            new_line = line.strip()
            if line.startswith("#Chr"):
                out.write(new_line+"\tgnomad_number_of_homozygotes\n")
                continue
            record = re.split("\t",new_line)
            #Chr    Start   End     Ref     Alt     gnomad41_genome_AF      gnomad41_genome_AF_raw  gnomad41_genome_AF_XX   gnomad41_genome_AF_XY   gnomad41_genome_AF_grpmax  gnomad41_genome_faf95   gnomad41_genome_faf99   gnomad41_genome_fafmax_faf95_max        gnomad41_genome_fafmax_faf99_max        gnomad41_genome_AF_afr     gnomad41_genome_AF_ami  gnomad41_genome_AF_amr  gnomad41_genome_AF_asj  gnomad41_genome_AF_eas  gnomad41_genome_AF_fin  gnomad41_genome_AF_mid     gnomad41_genome_AF_nfe  gnomad41_genome_AF_remaining    gnomad41_genome_AF_sas
            # 0      1       2       3       4
            key_str = "\t".join(record[0:5])
            if key_str in gnomad_nhomalt_dic:
                gnomad_number_of_homozygotes = gnomad_nhomalt_dic[key_str]
                out.write(new_line+"\t"+str(gnomad_number_of_homozygotes)+"\n")
            else:
                out.write(new_line+"\t-\n")

if __name__ == '__main__':
    main()
