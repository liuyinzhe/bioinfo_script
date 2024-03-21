#!/bin/bash
#https://ftp.ncbi.nlm.nih.gov/blast/db/
#2024-03-18
for i in {00..91}
do
    aria2c -c https://ftp.ncbi.nlm.nih.gov/blast/db/nr.${i}.tar.gz
    aria2c -c https://ftp.ncbi.nlm.nih.gov/blast/db/nr.${i}.tar.gz.md5
    md5sum -c nr.${i}.tar.gz.md5 && tar -zxvf nr.${i}.tar.gz && rm -rf nr.${i}.tar.gz echo "nr.${i} has done."
done
