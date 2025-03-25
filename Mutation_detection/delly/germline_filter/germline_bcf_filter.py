import os
import sys
import re
import pickle
import pysam
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
        if child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst


def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    pwd = Path().cwd()#.parent # 项目目录
    delly_sv_filter_flag = False
    delly_sv_variation_dic = {}
    if len(sys.argv) >1:
        delly_sv_filter_flag = True
        sv_filter_pkl = Path(sys.argv[1])
        delly_sv_variation_dic = pickle.load(open(sv_filter_pkl, 'rb'))
    # INS_dic = delly_sv_variation_dic["INS"]
    # DEL_dic = delly_sv_variation_dic["DEL"]
    # INV_dic = delly_sv_variation_dic["INV"]
    # DUP_dic = delly_sv_variation_dic["DUP"]
    # BND_dic = delly_sv_variation_dic["BND"]

    germline_bcf_list = GetAllFilePaths(pwd,wildcard='*.germline.unfiltered.bcf')
    #germline_bcf_list = GetAllFilePaths(pwd,wildcard='*.germline.unfilter.bcf')
    germline_bcf = germline_bcf_list[0]
    sample_name = re.split(r"\.",germline_bcf.name)[1]
    # 打开输入的VCF文件
    vcf_in = pysam.VariantFile(germline_bcf, mode="r")
    
    # delly.B120240901C19D39002.germline.PASS.vcf.gz
    os.chdir(pwd)
    out_bcf = pwd.joinpath("delly.{sample_name}.germline.PASS.bcf".format(sample_name=sample_name))
    print(out_bcf)
    # 创建输出的压缩VCF文件，使用原文件的头信息
    vcf_out = pysam.VariantFile(out_bcf, mode="wb", header=vcf_in.header)

    # 遍历每条记录
    for record in vcf_in:
        # 过滤条件1: 保留PRECISE的记录
        if 'PRECISE' not in record.info:
            continue
        '''
        #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT
                                        alts[0]         filter  info
                                    [chr10:125907524[C
        '''
        # 过滤条件2: 保留FILTER为PASS的记录
        if list(record.filter) != ['PASS']:
            continue
        
        # # 过滤条件3: PE和SR总和 >= 10
        # pe = record.info.get('PE', 0)
        # sr = record.info.get('SR', 0)
        # if (pe + sr) < 10:
        #     continue
        
        # 过滤条件4: 删除DUP类型
        # svtype = record.info.get('SVTYPE', '')
        # if svtype == 'DUP':
        #     continue

        sv_type = record.info.get('SVTYPE', '')
        
        if  delly_sv_filter_flag :
            if sv_type in ["DUP","INV"]:
                # chr10,pos,end,ref,type
                #print(record.chrom,record.pos,record.stop,record.ref,sv_type)
                info_list = [record.chrom,record.pos,record.stop,record.ref,sv_type]
                info_str = '\t'.join(list(map(str,info_list)))
                if info_str in delly_sv_variation_dic[sv_type]:
                    #print("x")
                    continue
            elif sv_type in ["INS","DEL"]:
                #print(record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type)
                info_list = [record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type]
                info_str = '\t'.join(list(map(str,info_list)))
                if info_str in delly_sv_variation_dic[sv_type]:
                    #print("y")
                    continue
            elif sv_type == "BND":
                # chr10,pos,end,ref,alt,type,chr2 pos2
                #print(record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type,record.info["CHR2"],record.info["POS2"])
                info_list = [record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type,record.info["CHR2"],record.info["POS2"]]
                info_str = '\t'.join(list(map(str,info_list)))
                if info_str in delly_sv_variation_dic[sv_type]:
                    #print("z")
                    continue
        
        # 写入符合条件的记录
        vcf_out.write(record)

    # 关闭文件
    vcf_in.close()
    vcf_out.close()
    # 先确保 BCF 文件已按染色体和位置排序
    pysam.tabix_index(str(out_bcf), 
                   force=True,
                   preset="vcf", 
                   keep_original=True)  # 关键参数


if __name__ == '__main__':
    main()
