import gzip
import sys
import re
import os
from pathlib import Path

#curl -o fastq.gz https://trace.ncbi.nlm.nih.gov/Traces/sra-reads-be/fastq?acc=SRR8292599


## 跳转脚本所在目录
#pwd = os.path.split(os.path.realpath(__file__))[0]
pwd = os.getcwd() # 执行目录
pwd = Path(pwd)
os.chdir(pwd)

input_name = sys.argv[1] # SRR8292599.fastq.gz
sample=re.sub(r".fastq.gz","",input_name)
line_count=0
unit_str = ""
read_flag =''
#with gzip.open(sys.argv[1],mode='rt',encoding='utf-8') as fh,gzip.open(sample+".1.fq.gz",mode='wb') as out1,gzip.open(sample+".2.fq.gz",mode='wb') as out2:
with gzip.open(sys.argv[1],mode='rt') as fh,gzip.open(sample+".1.fq.gz",mode='wb') as out1,gzip.open(sample+".2.fq.gz",mode='wb') as out2:
    for line in fh:
        line_count+=1
        if line_count%4==1 and line.startswith("@"): #ID
            
            match_num_obj =re.search(r"@"+sample+"\.\d{1,}\.(\d{1}) ",line)
            if match_num_obj:
                # 替换修改
                line="@"+re.split(" ",line,maxsplit=1)[1]
                unit_str +=line
                if match_num_obj.group(1) =="1":
                    read_flag ='1'
                elif match_num_obj.group(1) =="2":
                    read_flag ='2'
            else:
                #匹配不到，可能是单端
                print("无法匹配reads 编号")
                exit()
        elif line_count%4==2: # seq
            unit_str +=line
        elif line_count%4==3 and line.startswith("+"): #+
            unit_str +="+\n"
        elif line_count%4==0 and read_flag != "": # 质量值
            unit_str +=line
            if read_flag == "1":
                out1.write(bytes(unit_str.encode()))
                read_flag=""
                unit_str=""
            elif read_flag == "2":
                out2.write(bytes(unit_str.encode()))
                read_flag=""
                unit_str=""
            else:
                #匹配的数字超过2
                print('format err2:',sample)
                
        else:
            print('format err1:',sample)
