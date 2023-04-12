
# -f 比例
seqtk seq -s 11 -f 0.6805888 $dir/CNR01/WGS.read1.fq.gz |gzip >new_r1.fq.gz
seqtk seq -s 11 -f 0.6805888 $dir/CNR01/WGS.read2.fq.gz |gzip >new_r2.fq.gz

# reads 条数
seqtk sample -s 11 $dir/read1.fq.gz 1000000 |gzip  > sub_r1.fq.gz
seqtk sample -s 11 $dir/read2.fq.gz 1000000 |gzip  > sub_r2.fq.gz
