import os
import re
import pysam
import pickle
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


'''
hg38版本 delly
(1) 批量读取对照样品进行过滤，存储坐标和变异序列
(2) 存储 pkl 
(3) 过滤时，读取pkl
    当set 元素重复时,过滤
'''
def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    current_dir = Path().cwd()#.parent # 项目目录

    # 存储字典
    delly_sv_variation_dic = {
                                "INV":set(),
                                "DUP":set(),
                                "INS":set(),
                                "DEL":set(),
                                "BND":set(),# 记录变异统计次数,变异分类,存储info
                                'source':dict(), # 记录来源 info:来源样品名,列表 {info:[sampleA,sampleB]}
                              }
    
    germline_bcf_list = GetAllFilePaths(current_dir,wildcard='*.germline.unfilter.bcf')
    for germline_bcf in germline_bcf_list:
        # delly.S003.germline.filtered.bcf
        sample_name = re.split(r"\.",germline_bcf.name)[1]
        # 打开输入的VCF文件
        with pysam.VariantFile(germline_bcf, mode="r") as vcf_in:
            '''
            .chrom: 返回字符串
            .pos: 返回数值。 这个是以0为基, 可以用.start和.stop
            .id: 如果无记录, 就是NoneType
            .ref: 返回字符串
            .alts: 返回元祖(tuple), 因为一个位点上可以有多个变异类型
            .qual: 返回数值
            .filter: 返回pysam.libcbcf.VariantRecordFilter对象, 类似于字典
            .info: 返回pysam.libcbcf.VariantRecordInfo对象，类似于字典, 存放所有样本的统计信息
            .format: 返回pysam.libcbcf.VariantRecordFormat，类似于字典, 存放后续每个样本数据存放顺序和数据类型
            .samples: 返回pysam.libcbcf.VariantRecordSamples, 类似于字典, 存放每一个样本的具体信息
            '''
            # 遍历每条记录
            for record in vcf_in:
                # 过滤条件1: 保留PRECISE的记录
                if 'PRECISE' not in record.info:
                    continue
                #print(dict(record.info))
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

                '''
                # database
                # DUP INV
                chr10,pos,end,ref,type
                #INS DEL
                chr10,pos,end,ref,alt,type
                #BND
                chr10,pos,end,ref,alt,type,chr2 pos2
                '''
                if sv_type in ["DUP","INV"]:
                    # chr10,pos,end,ref,type
                    #print(record.chrom,record.pos,record.stop,record.ref,sv_type)
                    info_list = [record.chrom,record.pos,record.stop,record.ref,sv_type]
                    info_str = '\t'.join(list(map(str,info_list)))
                    delly_sv_variation_dic[sv_type].add(info_str)

                    #记录来源
                    if info_str not in delly_sv_variation_dic['source']:
                        delly_sv_variation_dic['source'][info_str]=[sample_name,]
                    else:
                        delly_sv_variation_dic['source'][info_str].append(sample_name)

                elif sv_type in ["INS","DEL"]:
                    #print(record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type)
                    info_list = [record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type]
                    info_str = '\t'.join(list(map(str,info_list)))
                    delly_sv_variation_dic[sv_type].add(info_str)

                    #记录来源
                    if info_str not in delly_sv_variation_dic['source']:
                        delly_sv_variation_dic['source'][info_str]=[sample_name,]
                    else:
                        delly_sv_variation_dic['source'][info_str].append(sample_name)

                elif sv_type == "BND":
                    # chr10,pos,end,ref,alt,type,chr2 pos2
                    #print(record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type,record.info["CHR2"],record.info["POS2"])
                    info_list = [record.chrom,record.pos,record.stop,record.ref,record.alts[0],sv_type,record.info["CHR2"],record.info["POS2"]]
                    info_str = '\t'.join(list(map(str,info_list)))
                    delly_sv_variation_dic[sv_type].add(info_str)

                    #记录来源
                    if info_str not in delly_sv_variation_dic['source']:
                        delly_sv_variation_dic['source'][info_str]=[sample_name,]
                    else:
                        delly_sv_variation_dic['source'][info_str].append(sample_name)
    # 序列化
    with open("dict.pkl", 'wb') as write:
        pickle.dump(delly_sv_variation_dic, write)
    
    for key,value_lst in delly_sv_variation_dic["source"].items():
        if len(value_lst)>1 and value_lst != ['Fibroblast_FIA240201', 'FIA240401']:
            print(key,value_lst)
    # # 反序列化
    # delly_sv_variation_dic = pickle.load(open("dict.pkl", 'rb'))
    # print(delly_sv_variation_dic)

if __name__ == '__main__':
    main()
