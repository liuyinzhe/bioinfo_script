#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd
import re
import sys
import math

'''
@File    :   psl2tsv.py
@Time    :   2023/12/18 14:25:02
@Author  :   lyz 
@Version :   1.0
@Desc    :   psl 结果排序，最佳比对
'''


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

def row2variable_lst(row,columns_lst):
    return_lst = []
    for col in columns_lst:
        return_lst.append(row[col])
    return return_lst

def pslIsProtein(blockCount, strand, tStart, tEnd, tSize, tStarts, blockSizes):
    starts = re.split(',',tStarts)
    sizes = re.split(',',blockSizes)
    lastBlock = blockCount - 1
    answer = 1
    if len(strand) > 1:
        direction = strand[1]
        if direction == "+":
            test = starts[lastBlock] + (3 * sizes[lastBlock])
            answer = 3 if tEnd == test else 1
        elif direction == "-":
            test = tSize - (starts[lastBlock] + (3 * sizes[lastBlock]))
            answer = 3 if tStart == test else 1
    return answer


def pslCalcMilliBad(sizeMul, qEnd, qStart, tEnd, tStart, qNumInsert, tNumInsert, matches, repMatches, misMatches, isMrna):
    milliBad = 0
    qAliSize = sizeMul * (qEnd - qStart)
    tAliSize = tEnd - tStart
    aliSize = qAliSize
    aliSize = tAliSize if tAliSize < qAliSize else aliSize
    if aliSize <= 0:
        return milliBad
    sizeDif = qAliSize - tAliSize
    if sizeDif < 0:
        if isMrna:
            sizeDif = 0
        else:
            sizeDif = -sizeDif
    insertFactor = qNumInsert
    if not isMrna:
        insertFactor += tNumInsert
    total = sizeMul * (matches + repMatches + misMatches)
    if total != 0:
        roundAwayFromZero = 3 * math.log(1 + sizeDif)
        if roundAwayFromZero < 0:
            roundAwayFromZero = int(roundAwayFromZero - 0.5)
        else:
            roundAwayFromZero = int(roundAwayFromZero + 0.5)
        milliBad = (1000 * (misMatches * sizeMul + insertFactor + roundAwayFromZero)) / total
    return milliBad

'''
while (my $file = shift) {
  if ($file =~ m/.gz$/) {
    open (FH, "zcat $file|") or die "can not read $file";
  } else {
    open (FH, "<$file") or die "can not read $file";
  }
  while (my $line = <FH>) {
    next if ($line =~ m/^#/);
    chomp $line;
    my ($matches, $misMatches, $repMatches, $nCount, $qNumInsert, $qBaseInsert, $tNumInsert, $tBaseInsert, $strand, $qName, $qSize, $qStart, $qEnd, $tName, $tSize, $tStart, $tEnd, $blockCount, $blockSizes, $qStarts, $tStarts) = split('\t', $line);
    my $sizeMul = pslIsProtein($blockCount, $strand, $tStart, $tEnd, $tSize, $tStarts, $blockSizes);
    my $pslScore = $sizeMul * ($matches + ( $repMatches >> 1) ) -
        $sizeMul * $misMatches - $qNumInsert - $tNumInsert;
    my $milliBad = int(pslCalcMilliBad($sizeMul, $qEnd, $qStart, $tEnd, $tStart, $qNumInsert, $tNumInsert, $matches, $repMatches, $misMatches, 1));
    my $percentIdentity = 100.0 - $milliBad * 0.1;
    printf "%s\t%d\t%d\t%s:%d-%d\t%d\t%.2f\n", $tName, $tStart, $tEnd, $qName, $qStart, $qEnd, $pslScore, $percentIdentity;

  }
  close (FH);
}
'''

def calculate_score(row,columns_list):
    matches,misMatches,repMatches,nCount,qNumInsert,\
    qBaseInsert,tNumInsert,tBaseInsert,strand,qName,\
    qSize,qStart,qEnd,tName,tSize,tStart,tEnd,blockCount,\
    blockSizes,qStarts,tStarts = row2variable_lst(row,columns_list)

    sizeMul = pslIsProtein(blockCount, strand, tStart, tEnd, tSize, tStarts, blockSizes)
    pslScore = sizeMul * (matches + ( repMatches >> 1) ) -sizeMul * misMatches - qNumInsert - tNumInsert
    #print(pslScore)
    return pslScore


def calculate_percentIdentity(row,columns_list):
    matches,misMatches,repMatches,nCount,qNumInsert,\
    qBaseInsert,tNumInsert,tBaseInsert,strand,qName,\
    qSize,qStart,qEnd,tName,tSize,tStart,tEnd,blockCount,\
    blockSizes,qStarts,tStarts = row2variable_lst(row,columns_list)

    sizeMul = pslIsProtein(blockCount, strand, tStart, tEnd, tSize, tStarts, blockSizes)
    milliBad = int(pslCalcMilliBad(sizeMul, qEnd, qStart, tEnd, tStart, qNumInsert, tNumInsert, matches, repMatches, misMatches, 1))
    percentIdentity = 100.0 - milliBad * 0.1
    #print(percentIdentity)
    return percentIdentity

def calculate_score_ident(row,columns_list):
    matches,misMatches,repMatches,nCount,qNumInsert,\
    qBaseInsert,tNumInsert,tBaseInsert,strand,qName,\
    qSize,qStart,qEnd,tName,tSize,tStart,tEnd,blockCount,\
    blockSizes,qStarts,tStarts = row2variable_lst(row,columns_list)

    sizeMul = pslIsProtein(blockCount, strand, tStart, tEnd, tSize, tStarts, blockSizes)
    pslScore = sizeMul * (matches + ( repMatches >> 1) ) -sizeMul * misMatches - qNumInsert - tNumInsert
    milliBad = int(pslCalcMilliBad(sizeMul, qEnd, qStart, tEnd, tStart, qNumInsert, tNumInsert, matches, repMatches, misMatches, 1))
    percentIdentity = 100.0 - milliBad * 0.1
    #print(pslScore,percentIdentity)
    return pslScore,percentIdentity

def calculate_Span(row,columns_list):
    matches,misMatches,repMatches,nCount,qNumInsert,\
    qBaseInsert,tNumInsert,tBaseInsert,strand,qName,\
    qSize,qStart,qEnd,tName,tSize,tStart,tEnd,blockCount,\
    blockSizes,qStarts,tStarts = row2variable_lst(row,columns_list)
    Span = abs(tEnd - tStart)
    return Span

def get_hit_info(input_psl,):
    parent_dir = input_psl.parent
    prefix_name = input_psl.stem
    out_all_tsv = Path.joinpath(parent_dir,prefix_name+'.all_hit.blat.sorted.tsv')
    out_best_hit_tsv = Path.joinpath(parent_dir,prefix_name+'.best_hit.blat.tsv')
    # 关于 blat score 的计算
    # https://genome.ucsc.edu/FAQ/FAQblat.html#blat4
    # Replicating web-based Blat percent identity and score calculations
    # 参考以下脚本
    # https://genome-source.gi.ucsc.edu/gitlist/kent.git/raw/master/src/utils/pslScore/pslScore.pl
    # 
    # https://www.cnblogs.com/pennyy/p/4260934.html

    # Downloading BLAT source and documentation
    # https://genome.ucsc.edu/FAQ/FAQblat.html#blat9
    # https://hgdownload.soe.ucsc.edu/admin/exe/
    # 
    # https://zhuanlan.zhihu.com/p/407911448
    blat_tbl_df = pd.read_table(input_psl, skiprows=5, header= None)# skiprows可用于跳过文件前几个注释行。

    # 重命名
    blat_tbl_df.columns=["matches","misMatches","repMatches","nCount","qNumInsert",
                                "qBaseInsert","tNumInsert","tBaseInsert","strand","qName",
                                "qSize","qStart","qEnd","tName","tSize","tStart","tEnd",
                                "blockCount","blockSizes","qStarts","tStarts"]

    columns_list = columns_list = ["matches","misMatches","repMatches","nCount","qNumInsert",
                                "qBaseInsert","tNumInsert","tBaseInsert","strand","qName",
                                "qSize","qStart","qEnd","tName","tSize","tStart","tEnd",
                                "blockCount","blockSizes","qStarts","tStarts"]
    #print(blat_tbl_df.shape)

    #blat_tbl_df['Score'],blat_tbl_df['Identity'] = blat_tbl_df.apply(calculate_score_ident, axis=1, args=(columns_list,))
    blat_tbl_df['Score'] = blat_tbl_df.apply(calculate_score, axis=1, args=(columns_list,))
    blat_tbl_df['Identity'] = blat_tbl_df.apply(calculate_percentIdentity, axis=1, args=(columns_list,))
    blat_tbl_df['Span'] = blat_tbl_df.apply(calculate_Span, axis=1, args=(columns_list,))

    #print(blat_tbl_df.shape)

    #blat_tbl_df = blat_tbl_df.apply(add_score_column, axis=1, args=(columns_list,))
    #new_columns = ["Score","Identity","Span"] +columns_list 

    # #QUERY   SCORE START   END QSIZE IDENTITY  CHROM              STRAND  START       END   SPAN

    new_columns = ["qName","Score","qStart","qEnd","qSize","Identity","tName","strand","tStart","tEnd","tSize","Span",
                    "matches","misMatches","repMatches","nCount",
                    "qNumInsert","qBaseInsert","tNumInsert","tBaseInsert",
                    "blockCount","blockSizes","qStarts","tStarts"]
    blat_tbl_df = blat_tbl_df[new_columns]
    #print(blat_tbl_df)


    # 全部输出
    blat_tbl_sortby_qName_df = blat_tbl_df.sort_values(by=['qName','Score'],ascending=[True, False],inplace=False)    ##按照query name排序

    blat_tbl_sortby_qName_df.to_csv(out_all_tsv, sep="\t", index=None)

    #Score 排序,根据qName去重,保留最好比对
    best_hit = blat_tbl_sortby_qName_df.sort_values(by=['Score'], ascending= False).drop_duplicates(subset='qName')  #对于每个query序列，按照 Score降序排序（ ascending= False)），排在第一位的是最佳比对结果； drop_duplicates去除其他比对结果。

    best_hit.to_csv(out_best_hit_tsv, sep="\t", index=None)

def main():
    # script_path =Path(__file__)
    # script_dir = Path(script_path).parent
    # print(script_dir)
    current_dir = Path.cwd()
    files_lst = GetAllFilePaths(current_dir,wildcard='*.psl')
    for input_psl in files_lst:
        get_hit_info(input_psl)




if __name__ == '__main__':
    main()
