
### 工具准备
```bash
wget http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/gtfToGenePred
chmod 755 gtfToGenePred
```
### 数据下载
```bash
#wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz  # 2020-08-17 18:56 版本
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/ncbiRefSeq.txt.gz # 2024-09-11 08:32 版本
# ncbiRefSeq.txt.gz 的版本更新，基因名更新更多一些

# 从gtf转为txt.gz(GenePred table format,RefGene)
#wget https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/hg38.refGene.gtf.gz
#wget https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/genes/hg38.ncbiRefSeq.gtf.gz
```
### 从gtf转为RefGene
```bash
./binary/gtfToGenePred  -genePredExt hg38.ncbiRefSeq.gtf  hg38_refGene.txt
```
- [x] 缺点:少了第一列数据库中的id;annovar 可以识别

### 数据处理(从RefGene)
```bash
zcat ncbiRefSeq.txt.gz > hg38_refGene.txt

grep -v _alt hg38_refGene.txt > hg38_refGene.txt2
grep -v "_fix" hg38_refGene.txt2 >hg38_refGene.txt3
grep -v "chrUn_" hg38_refGene.txt3 >hg38_refGene.txt4
grep -v "_random" hg38_refGene.txt4 > hg38_refGene.txt5
mv hg38_refGene.txt5 hg38_refGene.txt
# refGene.txt.gz 直接解压
```
### 生成hg38_refGeneMrna.fa
```bash
/data/software/annovar/retrieve_seq_from_fasta.pl \
  --format refGene \
  --seqfile /data/database/genome/ucsc/hg38.fa hg38_refGene.txt \
  --out hg38_refGeneMrna.fa
```
