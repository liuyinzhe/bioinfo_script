
from cyvcf2 import VCF
from pathlib import Path
import gzip

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
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()
    vcf_file_lst = GetAllFilePaths(current_dir,'*.vcf.bgz')
    for vcf_file in vcf_file_lst:
        tab_file = vcf_file.with_suffix("").with_suffix(".txt.gz")
        with gzip.open(tab_file,'wt',encoding='utf-8') as out:
            out.write("chrom\tstart\tstop\tref\talt\tallele_type\tAF\tAF_eas\tnhomalt\n")
            for variant in VCF(vcf_file):
                # chrom   start   stop    ref     alt
                ref_seq = variant.REF # e.g. REF='A', 
                alt_seq = variant.ALT # e.g. ALT=['C', 'T']
                if type(alt_seq) == list:
                    alt_seq = ",".join([x for x in alt_seq])
                chrom = variant.CHROM
                start = variant.start
                end = variant.end
                # variant_id = variant.ID
                # filter_string = variant.FILTER
                # variant_qual = variant.QUAL

                ## INFO Field.
                ## extract from the info field by it's name:
                
                #     allele_type     AF      AF_eas  nhomalt
                info_AF = variant.INFO.get('AF') # float
                info_AF_eas = variant.INFO.get('AF_eas') # float
                info_nhomalt = variant.INFO.get('nhomalt') # int
                info_allele_type = variant.INFO.get('allele_type') # str
                out.write("\t".join([chrom,str(start+1),str(end),ref_seq,alt_seq,info_allele_type,str(info_AF),str(info_AF_eas),str(info_nhomalt)]) + "\n")
                # {'INDEL': True, 'IDV': 1, 'IMF': 0.012345699593424797, 'DP': 81, 'I16': (45.0, 18.0, 1.0, 0.0, 3713.0, 231795.0, 54.0, 2916.0, 3780.0, 226800.0, 60.0, 3600.0, 1303.0, 31025.0, 8.0, 64.0), 'QS': (0.9843840003013611, 0.015615999698638916), 'VDB': 0.47082599997520447, 'SGB': -0.3798849880695343, 'MQSB': 1.0, 'MQ0F': 0.0}
                # # convert back to a string.
                # print(str(variant)) # 整行内容



if __name__ == '__main__':
    main()

