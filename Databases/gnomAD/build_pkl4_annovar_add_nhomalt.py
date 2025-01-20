import pandas as pd
from pathlib import Path
import gzip
import pickle
import polars as pl

import sys
import time
import datetime
import logging
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "#配置输出日志格式
#配置输出时间的格式，注意月份和天数不要搞乱了
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %A ' #'%Y-%m-%d  %H:%M:%S' 



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
            files_lst.append(str(child))
    return files_lst

def main():
    script_path =Path(__file__)
    script_dir = Path(script_path).parent
    #print(script_dir)
    current_dir = Path.cwd()
    logging_out = current_dir.joinpath('logging.log')
    # logging
    # 默认生成的 root logger 的 level 是 logging.WARNING，低于该级别的就不输出了。
    # 级别排序：CRITICAL > ERROR > WARNING > INFO > DEBUG。（如果需要显示所有级别的内容，可将 level=logging.NOTSET）
    #设置输出格式
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt = DATE_FORMAT,
                        filename=logging_out,
                        filemode='w'
                        )


    # 文件
    output_gzip_pkl = current_dir.joinpath('gnomad_nhomalt_dic.pkl.gz')
    gnomad_txt_lst = GetAllFilePaths(current_dir,'*.txt.gz')

    gnomad_nhomalt_dic = {}
    for gzip_txt in gnomad_txt_lst:
        '''
        chrom   start   stop    ref     alt     allele_type     AF      AF_eas  nhomalt
        '''
        # 全部列用String 类型，否则需要用字典映射指定 dtypes={name:pl.Int32,name2:pl.String}
        vcf_df = pl.read_csv(gzip_txt,separator='\t',infer_schema_length=0).with_columns(pl.all().cast(pl.String, strict=False))# pl.Int32 # pl.String
        chrom_lst = vcf_df["chrom"]
        start_lst = vcf_df["start"]
        stop_lst = vcf_df['stop']
        ref_lst = vcf_df['ref']
        alt_lst = vcf_df['alt']
        nhomalt_lst = vcf_df['nhomalt']
        allele_type_lst = vcf_df['allele_type']
        # polars dataframe 按行遍历
        for row in zip(chrom_lst,start_lst,stop_lst,ref_lst,alt_lst,nhomalt_lst,allele_type_lst):
            chrom ,start,stop,ref ,alt ,nhomalt,allele_type  = row
            if allele_type == 'snv':
                key_str = "\t".join([chrom,start,stop,ref,alt])
                if key_str not in gnomad_nhomalt_dic:
                    gnomad_nhomalt_dic[key_str] = nhomalt
                else:
                    logging.info("snv 重复,{}".format(key_str))
                    # print("snv 重复",key_str)
            else:
                # 直接存储
                key_str = "\t".join([chrom,start,stop,ref,alt])
                if key_str not in gnomad_nhomalt_dic:
                    gnomad_nhomalt_dic[key_str] = nhomalt
                else:
                    logging.info("indel 重复,{}".format(key_str))
                    #print("indel 重复",key_str)
                # 处理
                '''
                    # del
                    chr1    10109   10114   AACCCT  -
                    chr1    10108   10114   CAACCCT C 

                    # ins
                    chr1    10108   10108   -       A 
                    chr1    10108   10108   C       CA 
                '''
                if allele_type == 'del':
                    alt = '-'
                    ref = ref[1:]
                    key_str = "\t".join([chrom,start,stop,ref,alt])
                    if key_str not in gnomad_nhomalt_dic:
                        gnomad_nhomalt_dic[key_str] = nhomalt
                    else:
                        logging.info("del 重复,{}".format(key_str))
                        #print("del 重复",key_str)
                elif allele_type == 'ins':
                    ref = '-'
                    alt = alt[1:]
                    key_str = "\t".join([chrom,start,stop,ref,alt])
                    if key_str not in gnomad_nhomalt_dic:
                        gnomad_nhomalt_dic[key_str] = nhomalt
                    else:
                        logging.info("ins 重复,{}".format(key_str))
                        #print("ins 重复",key_str)
        # 
        current_time = datetime.datetime.now()

        # 格式化时间为年月日时分秒
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        logging.info("处理完成,{gzip_txt};{formatted_time}".format(gzip_txt=gzip_txt,formatted_time=formatted_time))
    logging.info("序列化压缩中...")
    # 序列化
    with gzip.open(output_gzip_pkl,mode='wb') as pkl_gz:
        pickle.dump(gnomad_nhomalt_dic, pkl_gz)
    # df.to_pickle(file_path='data.pkl', compression='gzip')
    # # 反序列化
    # with gzip.open('gnomad_nhomalt_dic.pkl.gz', mode='rb') as pkl_gz:
    #     deserialization = pickle.load(pkl_gz)
    # deserialization = pickle.load(open("dict.pkl", 'rb'))
    # print(deserialization)
    pass

if __name__ == '__main__':
    if sys.version[0] == "3":
        start_time = time.perf_counter()
    else:
        start_time = time.clock()
    main()
    if sys.version[0] == "3":
        end_time = time.perf_counter()
    else:
        end_time = time.clock()
    print("%s %s %s\n" % ("main()", "use", str(
        datetime.timedelta(seconds=end_time - start_time))))
    logging.info("%s %s %s\n"%("main()", "use", str(datetime.timedelta(seconds = end_time - start_time))))
