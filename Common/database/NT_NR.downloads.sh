#!/bin/bash

# NR
#https://ftp.ncbi.nlm.nih.gov/blast/db/
for i in {00..82}
do
    wget -c https://ftp.ncbi.nlm.nih.gov/blast/db/nr.${i}.tar.gz
    wget -c https://ftp.ncbi.nlm.nih.gov/blast/db/nr.${i}.tar.gz.md5
    md5sum -c nr.${i}.tar.gz.md5
    tar -zxvf nr.${i}.tar.gz -C
    echo "nr.${i} has done."
done

# # NT
# #https://ftp.ncbi.nlm.nih.gov/blast/db/
# for i in {00..113}
# do
#     /bin/wget -c https://ftp.ncbi.nlm.nih.gov/blast/db/nt.${i}.tar.gz
#     /bin/wget -c https://ftp.ncbi.nlm.nih.gov/blast/db/nt.${i}.tar.gz.md5
#     md5sum -c nt.${i}.tar.gz.md5
#     tar -zxvf nt.${i}.tar.gz -C
#     echo "nt.${i} has done."
# done
