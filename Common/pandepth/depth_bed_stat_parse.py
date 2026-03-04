#!/usr/bin/env python3

import gzip
import sys
import re
import time
import datetime
import argparse
from pathlib import Path
#import subprocess
#import pysam
#from multiprocessing import Pool
import numpy as np
import statistics

def GetAllFilePaths(directory,wildcard='*'):
    '''
    获取目录下文件全路径，通配符检索特定文件名，返回列表
    param: str  "directory"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    target_path=Path(directory)
    for child in target_path.rglob(wildcard):
        if child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst

def calc_CV(input_lst):
    mean = np.mean(input_lst)
    # 计算标准偏差
    variance = np.std(input_lst)
    cv_value = (variance/mean)*100
    return cv_value

def calc_CV_stat(data):
    # 计算平均值
    mean = statistics.mean(data)
    # 计算标准差
    std_dev = statistics.stdev(data)
    # 计算变异系数
    coefficient_of_variation = (std_dev / mean) * 100
    return coefficient_of_variation


def calc_Uniformity(wes_depth_lst,percentage=0.2):
    failed_id = []
    mean_value = np.mean(wes_depth_lst)
    all_count  = 0 
    count  = 0 
    for mean_depth in wes_depth_lst:
        all_count += 1
        if mean_depth < mean_value * percentage:
            failed_id
            continue
        count += 1
    
    #
    perc_result = count/all_count
    
    return perc_result

def calc_result_Uniformity(result_lst,wes_depth_lst,percentage=0.2):

    failed_id_lst = []
    mean_value = np.mean(wes_depth_lst)
    all_count  = 0 
    count  = 0 
    for name_id,mean_depth in result_lst:
        all_count += 1
        if mean_depth < mean_value * percentage:
            failed_id_lst.append(name_id)
            continue
        count += 1
    
    #
    perc_result = (count/all_count) * 100
    
    return perc_result,failed_id_lst


def main():
    script_path =Path(__file__).resolve()
    script_dir = Path(script_path).parent
    current_dir = Path.cwd()
    result_dic = {}
    gz_file_list = GetAllFilePaths(current_dir,wildcard='*.bed.stat.gz')
    ###RegionLength: 100997897       CoveredSite: 100381063  Coverage(%): 99.39      MeanDepth: 148.41
    match_compile = re.compile("##RegionLength: (\d+)\s+?CoveredSite: (\d+)\s+?Coverage\(%\): ([\d.]+)\s+?MeanDepth: ([\d.]+)")
    for gz_file in gz_file_list:
        file_name = gz_file.name
        sample_name = re.split(r"\.",file_name)[0]
        result_lst = []
        wes_depth_lst = [] # 记录平均深度，用于计算 CV 变异系数
        #原始统计信息
        fh=gzip.GzipFile(gz_file,mode="rb")
        stat_mean_depth = ""
        stat_coverage = ""
        for byte_line in fh:
            line = byte_line.decode('utf-8')
            if line.startswith("##RegionLength"):
                
                '''
                ##RegionLength: 100997897       CoveredSite: 100381063  Coverage(%): 99.39      MeanDepth: 148.41
                '''
                match_obj = match_compile.search(line)
                # print(line)
                # print("##MXM##",match_obj,type(line))
                if match_obj:
                    stat_mean_depth = float(match_obj.group(4))
                    stat_coverage = float(match_obj.group(3))
            elif line.startswith("#"):
                continue
            else:
                # #Chr    Start   End     RegionID        Length  CoveredSite     TotalDepth      Coverage(%)     MeanDepth
                #   0       1      2         3              4         5               6               7               8
                record = re.split("\t",line.strip())
                #print(record)
                name_id = record[3]
                MeanDepth = float(record[8])
                result_lst.append([name_id,MeanDepth])
                wes_depth_lst.append(MeanDepth)

            pass
        pass
        # 按照样品数据信息
        '''
        ##RegionLength: 100997897       CoveredSite: 100381063  Coverage(%): 99.39      MeanDepth: 148.41
        Fold-80 base penalty
        sample_name    mean_coverage    meanDepth    20%    50%   100%  CV

        80% > avg |= 1

        '''
        # cv_value = calc_CV(wes_depth_lst)
        cv_value_stat = calc_CV_stat(wes_depth_lst)
        #Uniformity20_value = calc_Uniformity(wes_depth_lst,0.2)
        Uniformity20_value,failed_id_20lst = calc_result_Uniformity(result_lst,wes_depth_lst,0.2)
        Uniformity50_value,failed_id_50lst = calc_result_Uniformity(result_lst,wes_depth_lst,0.5)
        Uniformity100_value,failed_id_100lst = calc_result_Uniformity(result_lst,wes_depth_lst,1)
        print(cv_value_stat,cv_value_stat,Uniformity20_value)#,failed_id_20lst)
        print("#",stat_mean_depth,stat_coverage)
        # 结果记录 {sample: MeanDepth\tCoverage(%)\tUniformity20(%)\tUniformity50(%)\tUniformity100(%)\tCoefficient_of_Variation(CV%)}
        # 格式化
        result_str = "{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format(stat_mean_depth,stat_coverage,Uniformity20_value,Uniformity50_value,Uniformity100_value,cv_value_stat)
        print(result_str)
        # 均一性
        if sample_name not in result_dic:
            result_dic[sample_name] =  result_str

        
    ## 输出内容
    with open("result.xls",mode='wt',encoding='utf-8') as out:
        out.write("Sample_Name\tMeanDepth\tCoverage(%)\tUniformity20(%)\tUniformity50(%)\tUniformity100(%)\tCoefficient_of_Variation(CV%)\n")
        for sample_name,result_str in result_dic.items():
            out.write(sample_name+"\t"+result_str+"\n")



if __name__ == "__main__":
    if sys.version[0] == "3":
        start_time = time.perf_counter()
    else:
        start_time = time.clock()
    main()
    if sys.version[0] == "3":
        end_time = time.perf_counter()
    else:
        end_time = time.clock()
    print("%s %s %s\n" % ("main()", "use", str(datetime.timedelta(seconds=end_time - start_time))))
