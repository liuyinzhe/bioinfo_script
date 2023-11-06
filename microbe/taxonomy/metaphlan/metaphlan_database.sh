aria2c -c -Z \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212.md5 \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212.tar \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212_marker_info.txt.bz2 \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212_species.txt.bz2


bowtie2-build --threads 20 \
  -f mpa_vOct22_CHOCOPhlAnSGB_202212.fna \
  mpa_vOct22_CHOCOPhlAnSGB_202212
