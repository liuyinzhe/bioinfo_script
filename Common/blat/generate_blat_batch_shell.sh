QC=#input file path
blat=#blat path
convert=# psl2tsv.py
work_path=# work path
query_seq=# input query.fa

rm -rf batch_blat.sh
while read sample ; do 
mkdir -p ${sample}
echo "PATH=/data/home/liuyinzhe/binary:$PATH ; \
  cd  ${work_path}/${sample} ; \
  /data/home/liuyinzhe/software/miniconda3/envs/microbe/bin/seqkit fq2fa  ${QC}/${sample}/${sample}.clean.1.fq.gz > ${work_path}/${sample}/${sample}.fa && \
  seqkit split  --by-size 20000000  --by-size-prefix tmp --force --out-dir ./  ${work_path}/${sample}/${sample}.fa && \
  rm -rf ${work_path}/${sample}/${sample}.fa && \
  ls *.fa |sed s/\.fa// |xargs -i faToTwoBit {}.fa {}.2bit && \
  rm -rf *.fa && \
  ls *.2bit |sed s/\.2bit// | xargs -i blat -stepSize=5 -repMatch=2253 -minScore=20 -minIdentity=0 {}.2bit  ${query_seq} {}.psl ;\
  ls *.psl  |xargs -i sed '1,5d' {} | sed '1iheader\n2\n3\n4\n5' > ${sample}.psl  ;\
  python ${convert} ${work_path}/${sample}/${sample}.psl ${work_path}/${sample}/${sample}.tsv && \
  rm -rf tmp* " >> batch_blat.sh
done < sample.lst
