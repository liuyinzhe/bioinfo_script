
bcftools norm 可以尝试替代 vt decompose/normalize 步骤
```python
   # normalize and left-align indels
   bcftools norm -f ref.fa in.vcf

   # split multi-allelic sites
   bcftools norm -m- in.vcf
```

### prepare_annovar_user.pl
>来自annovar Issue  https://github.com/WGLab/doc-ANNOVAR/issues/254
>>http://www.openbioinformatics.org/annovar/download/prepare_annovar_user.pl

### makeAnnovarIndex.pl
>索引文件生成脚本来自
>>https://github.com/pzweuj/practice/blob/master/perl/makeAnnovarIndex/makeAnnovarIndex.pl

参考:
https://pzweuj.github.io/2018/04/25/convert-clinvar-to-annovar.html
https://pzweuj.github.io/2018/07/27/annovar-clinvar.html
https://github.com/mobidic/update_annovar_db
https://github.com/ryuzheng/clinvar_db_for_annovar
