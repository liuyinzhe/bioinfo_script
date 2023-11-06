
### metaphlan3 databases
aria2c -c -Z \
http://cmprod1.cibio.unitn.it/biobakery3/metaphlan_databases/mpa_v31_CHOCOPhlAn_201901.md5 \
http://cmprod1.cibio.unitn.it/biobakery3/metaphlan_databases/mpa_v31_CHOCOPhlAn_201901.tar \
http://cmprod1.cibio.unitn.it/biobakery3/metaphlan_databases/mpa_v31_CHOCOPhlAn_201901_marker_info.txt.bz2 

# index
bowtie2-build --threads 20 \
  -f mpa_v31_CHOCOPhlAn_201901.fna \
  mpa_v31_CHOCOPhlAn_201901

# https://forum.biobakery.org/t/metaphlan4-mpa3-add-viruses-failed/4489
# metaphlan4 版本的数据库不包含病毒，未来4.1 版本才会支持 –mpa3 –add_viruses ,如果使用这俩参数，需要使用 metaphlan3 databases

### metaphlan4 databases
aria2c -c -Z \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212.md5 \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212.tar \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212_marker_info.txt.bz2 \
http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vOct22_CHOCOPhlAnSGB_202212_species.txt.bz2

# index
bowtie2-build --threads 20 \
  -f mpa_vOct22_CHOCOPhlAnSGB_202212.fna \
  mpa_vOct22_CHOCOPhlAnSGB_202212
