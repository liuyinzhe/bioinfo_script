#https://qiime.org/tutorials/source_tracking.html
# 需要过滤 只有 1%一下样品有内容的 ，因为这里例子 有700 样品，这里 -s 7 ,这里样品只有35 个所以不过滤

#filter_otus_from_otu_table.py -i otu_table.biom -o filtered_otu_table.biom -s 7
# 转格式
#biom convert -i filtered_otu_table.biom -o filtered_otu_table.txt -b


# 目录中要有 src
export SOURCETRACKER_PATH=/data/software/SourceTracker/sourcetracker-1.0.1

R --slave --vanilla --args \
    -i otu_table.txt \
    -m map.txt \
    -o sourcetracker_out < $SOURCETRACKER_PATH/sourcetracker_for_qiime.r
