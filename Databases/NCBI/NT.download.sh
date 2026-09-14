#!/bin/bash
#https://ftp.ncbi.nlm.nih.gov/blast/db/
#2024-03-20  135
#2026-09-07 376
for i in {000..376}
do
    aria2c -c https://ftp.ncbi.nlm.nih.gov/blast/db/nt.${i}.tar.gz
    aria2c -c https://ftp.ncbi.nlm.nih.gov/blast/db/nt.${i}.tar.gz.md5
    md5sum -c nt.${i}.tar.gz.md5 && tar -zxvf nt.${i}.tar.gz && rm -rf nt.${i}.tar.gz echo "nt.${i} has done."
done
