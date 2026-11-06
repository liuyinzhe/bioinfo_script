
### cache
```
# release-101
# https://ftp.ensembl.org/pub/release-101/variation/indexed_vep_cache/
# current
https://ftp.ensembl.org/pub/current/variation/indexed_vep_cache/
```
### Fasta
```
放到 cache 压缩包解压后的 "物种/组装版本/" 目录下
https://ftp.ensembl.org/pub/current/fasta/canis_lupus_familiarisgsd/dna/Canis_lupus_familiarisgsd.UU_Cfam_GSD_1.0.dna.toplevel.fa.gz
https://ftp.ensembl.org/pub/current/fasta/felis_catus/dna/Felis_catus.F.catus_Fca126_mat1.0.dna.toplevel.fa.gz
```

### 命令安装 cache/Fasta
```
# download cache file
vep_install -l -c /data/public/databases/vep_db
Do you want to continue installing the API (y/n)? n
Do you want to install any cache files (y/n)?y
# 选择安装：
#64 : canis_lupus_familiarisgsd_vep_116_UU_Cfam_GSD_1.0.tar.gz (110 MB)
#156 : felis_catus_vep_116_F.catus_Fca126_mat1.0.tar.gz (721 MB)


# download fasta file
vep_install -l -c /data/public/databases/vep_db
Do you want to continue installing the API (y/n)? n
Do you want to install any cache files (y/n)?n
Do you want to install any FASTA files (y/n)?y
# 选择安装：
#50 : canis_lupus_familiarisgsd
#111 : felis_catus
```

### Fasta 文件处理
```
gzip -d *.dna.toplevel.fa.gz
bgzip *.dna.toplevel.fa
```
