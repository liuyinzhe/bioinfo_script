

wget http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/liftOver #下载liftover
chomd +x ./liftover #更改下载的liftover的执行权限
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz #下载从hg19到hg38版转换的注释文件，其他的注释文件可以在http://hgdownload.soe.ucsc.edu/downloads.html#human中的LiftOver files下载


# hg19 -> hg38
./liftOver hg19_input.bed \
   hg19ToHg38.over.chain.gz \
   hg19tohg38_output.bed \
   hg19_unmapped.bed
