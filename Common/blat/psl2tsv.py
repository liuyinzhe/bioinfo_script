import pandas as pd
import sys

infile, outfile = sys.argv[1], sys.argv[2]



inp = pd.read_table(infile, skiprows=5, header= None)# skiprows可用于跳过文件前几个注释行。


inp.columns=["matches", "misMatches", "repMatches", "nCount", "qNumInsert", "qBaseInsert",
            "tNumInsert", "tBaseInsert", "strand", "qName", "qSize", "qStart", "qEnd", "tName", "tSize", "tStart", "tEnd",
            "blockCount", "blockSize", "qStarts", "tStarts"]
# 全部输出
output1 = inp.sort_values(by=['qName'])    ##按照query name排序

# matches 排序,根据qName去重,保留最好比对
# output2 = output1.sort_values(by=['matches'], ascending= False).drop_duplicates(subset='qName')  #对于每个query序列，按照 matches降序排序（ ascending= False)），排在第一位的是最佳比对结果； drop_duplicates去除其他比对结果。

output1.to_csv(outfile, sep="\t", index=None)
