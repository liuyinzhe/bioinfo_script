# web：
# https://genome.ucsc.edu/cgi-bin/hgBlat 

# faToTwoBit
# wget -c http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/faToTwoBit

# faToTwoBit genome.fa genome.2bit

# download:
# http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/

# reference genome:
#http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/hg19.2bit
#http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.2bit


# commond：
./blat -stepSize=5 -repMatch=2253 -minScore=20 -minIdentity=0 hg38.2bit xx.fa output.psl


#source# https://genome.ucsc.edu/FAQ/FAQblat.html#blat3

# get best hit
# https://www.jianshu.com/p/6d765e59aaf7
