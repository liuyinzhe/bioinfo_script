# # 小文件使用，条数
seqkit sample  \
  --quiet \
  --number  4 \
  --rand-seed 12 \
  --threads 2 \
  sample.clean.1.fq.gz \
   | gzip > sample.new.1.fq.gz
#   --out-file sample.new.1.fq

# 大文件使用，百分比
seqkit sample  \
  --quiet
  --proportion  0.8 \
  --rand-seed 12 \
  --threads 2 \
  sample.clean.1.fq.gz \
   | gzip > sample.new.1.fq.gz
#  --out-file sample.new.1.fq
  
# 大文件，行数
seqkit sample  \
 --rand-seed 123 \
 --proportion 0.9 \
 sample.2.fq.gz|seqkit head -n 100  |gzip >sample_new.2.fq.gz
