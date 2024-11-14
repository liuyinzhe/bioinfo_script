
#### build refGene
```shell
gffread new.gff -T -o new.gtf
gtfToGenePred -genePredExt new.gtf new.txt
perl ../retrieve_seq_from_fasta.pl --format refGene --seqfile new.fasta  new_refGene.txt --out new_refGeneMrna.fa

# result
#new_refGeneMrna.fa
#new_refGene.txt
```
### vcf2variant
```bash
perl ../convert2annovar.pl -format vcf4 BB3.HC.vcf > BB3.avinput
perl annotate_variation.pl -geneanno -dbtype refGene -out BB3 -build new BB3.avinput pepperdb/
# -geneanno  表示使用基于基因的注释
# -dbtype refGene  表示使用"refGene"类型的数据库
# -out new  表示输出以BB3为前缀的结果文件

perl annotate_variation.pl  -out BB3 -build new BB3.avinput pepperdb/
#BB3.exonic_variant_function #外显子区域突变的功能、类型等
#BB3.variant_function#突变的基因及位置
#BB3.log#日志文件
```

>代码来自 https://www.baishujun.com/archives/7476.html
