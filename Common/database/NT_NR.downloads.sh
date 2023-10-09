#!/bin/bash

# NR
#https://ftp.ncbi.nlm.nih.gov/blast/db/
for i in {00..82}
do
    wget -c -o nr.${i}.wget.log https://ftp.ncbi.nlm.nih.gov/blast/db/nr.${i}.tar.gz
    wget -c -o nr.${i}.md5.wget.log https://ftp.ncbi.nlm.nih.gov/blast/db/nr.${i}.tar.gz.md5
    md5sum -c nr.${i}.tar.gz.md5 && \
    tar -zxvf nr.${i}.tar.gz  && \
    echo "nr.${i} has done." && \
    rm -rf nr.${i}.tar.gz
done

# # NT
# #https://ftp.ncbi.nlm.nih.gov/blast/db/
# for i in {00..113}
# do
#     /bin/wget -c -o nr.${i}.wget.log https://ftp.ncbi.nlm.nih.gov/blast/db/nt.${i}.tar.gz
#     /bin/wget -c -o nr.${i}.md5.wget.log https://ftp.ncbi.nlm.nih.gov/blast/db/nt.${i}.tar.gz.md5
#     md5sum -c nt.${i}.tar.gz.md5 && \
#     tar -zxvf nt.${i}.tar.gz  && \
#     echo "nt.${i} has done." && \
#     rm -rf nt.${i}.tar.gz
# done
