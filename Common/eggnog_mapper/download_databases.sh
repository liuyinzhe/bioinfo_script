# https://www.jianshu.com/p/b93063302ed1

# aria2c
# aria2c -c -Z -P http://eggnog5.embl.de/download/emapperdb-5.0.2/{eggnog.db.gz,eggnog.taxa.tar.gz,eggnog_proteins.dmnd.gz,mmseqs.tar.gz,pfam.tar.gz}
# aria2c -c http://eggnog6.embl.de/download/novel_fams/novel_fams.dmnd.gz

# wget
wget http://eggnog5.embl.de/download/emapperdb-5.0.2/eggnog.db.gz
wget http://eggnog5.embl.de/download/emapperdb-5.0.2/eggnog.taxa.tar.gz
wget http://eggnog5.embl.de/download/emapperdb-5.0.2/eggnog_proteins.dmnd.gz
wget http://eggnog5.embl.de/download/emapperdb-5.0.2/mmseqs.tar.gz
wget http://eggnog5.embl.de/download/emapperdb-5.0.2/pfam.tar.gz
wget http://eggnog6.embl.de/download/novel_fams/novel_fams.dmnd.gz

# eggnog.db.gz			6G
# eggnog.taxa.tar.gz		69M
# eggnog_proteins.dmnd.gz		5G
# mmseqs.tar.gz			5G
# pfam.tar.gz			938M
# novel_fams.dmnd.gz    292M

gunzip eggnog.db.gz  && rm -rf eggnog.db.gz
tar -zxf eggnog.taxa.tar.gz  && rm -rf eggnog.taxa.tar.gz
gunzip eggnog_proteins.dmnd.gz && rm -rf eggnog_proteins.dmnd.gz
tar -zxf pfam.tar.gz && rm -rf pfam.tar.gz
tar -zxf mmseqs.tar.gz && rm -rf mmseqs.tar.gz
gunzip novel_fams.dmnd.gz && rm -rf novel_fams.dmnd.gz
