# hg19

./annotate_variation.pl -downdb -webfrom annovar knownGene --buildver hg19 ./humandb 
./annotate_variation.pl -downdb -webfrom annovar ensGene41 --buildver hg19 ./humandb >ensGene41.log 2>ensGene41.err

./annotate_variation.pl -downdb -webfrom annovar cytoBand --buildver hg19 ./humandb >cytoBand.log 2>cytoBand.err
./annotate_variation.pl -downdb -webfrom annovar 1000g2015aug --buildver hg19 ./humandb >1000g2015aug.log 2>1000g2015aug.err
./annotate_variation.pl -downdb -webfrom annovar avsnp150 --buildver hg19 ./humandb >avsnp150.log 2>avsnp150.err
./annotate_variation.pl -downdb -webfrom annovar cosmic68 --buildver hg19 ./humandb >cosmic68.log 2>cosmic68.err
./annotate_variation.pl -downdb -webfrom annovar clinvar_20221231 --buildver hg19 ./humandb >clinvar_20221231.log 2>clinvar_20221231.err
./annotate_variation.pl -downdb -webfrom annovar exac03 --buildver hg19 ./humandb >exac03.log 2>exac03.err
./annotate_variation.pl -downdb -webfrom annovar esp6500siv2_all --buildver hg19 ./humandb >esp6500siv2_all.log 2>esp6500siv2_all.err
./annotate_variation.pl -downdb -webfrom annovar intervar_20180118 --buildver hg19 ./humandb >intervar_20180118.log 2>intervar_20180118.err

./annotate_variation.pl -downdb -webfrom annovar ensGene41 --buildver hg19 ./humandb >ensGene41.log 2>ensGene41.err
./annotate_variation.pl -downdb -webfrom annovar dbnsfp42c --buildver hg19 ./humandb >dbnsfp42c.log 2>dbnsfp42c.err
./annotate_variation.pl -downdb -webfrom annovar exac03 --buildver hg19 ./humandb >ensGene41.log 2>ensGene41.err
./annotate_variation.pl -downdb -webfrom annovar  gnomad211_exome --buildver hg19 ./humandb >gnomad211_exome.hg38.log 2>gnomad211_exome.hg38.err
./annotate_variation.pl -downdb -webfrom annovar  gnomad211_genome --buildver hg19 ./humandb >gnomad211_genome.log 2>gnomad211_genome.err
./annotate_variation.pl -downdb -webfrom annovar  dbscsnv11 --buildver hg19 ./humandb >ensGene41.log 2>ensGene41.err
./annotate_variation.pl -downdb -webfrom annovar  ljb26_all --buildver hg19 ./humandb >ljb26_all.log 2>ljb26_all.err
./annotate_variation.pl -downdb -webfrom annovar  revel --buildver hg19 ./humandb >revel.log 2>revel.err

./annotate_variation.pl -downdb -webfrom annovar  dbnsfp47a_interpro --buildver hg19 ./humandb >dbnsfp47a_interpro.19.log 2>dbnsfp47a_interpro.19.err

./annotate_variation.pl -downdb rmsk --buildver hg19 ./humandb >rmsk.19.log 2>rmsk.19.err
# This rmsk annotation source is required by InterVar.
#https://github.com/WGLab/doc-ANNOVAR/issues/201

# hg38

./annotate_variation.pl -downdb -webfrom annovar knownGene --buildver hg38 ./humandb 
./annotate_variation.pl -downdb -webfrom annovar ensGene41 --buildver hg38 ./humandb >ensGene41.38.log 2>ensGene41.38.err

./annotate_variation.pl -downdb -webfrom annovar 1000g2015aug --buildver hg38 ./humandb >1000g2015aug.log 2>1000g2015aug.38.err
./annotate_variation.pl -downdb -webfrom annovar avsnp150 --buildver hg38 ./humandb >avsnp150.log 2>avsnp150.38.err
./annotate_variation.pl -downdb -webfrom annovar cosmic68 --buildver hg38 ./humandb >cosmic68.log 2>cosmic68.38.err
./annotate_variation.pl -downdb -webfrom annovar clinvar_20221231 --buildver hg38 ./humandb >clinvar_20221231.log 2>clinvar_20221231.38.err
./annotate_variation.pl -downdb -webfrom annovar exac03 --buildver hg38 ./humandb >exac03.log 2>exac03.38.err
./annotate_variation.pl -downdb -webfrom annovar esp6500siv2_all --buildver hg38 ./humandb >esp6500siv2_all.log 2>esp6500siv2_all.38.err
./annotate_variation.pl -downdb -webfrom annovar intervar_20180118 --buildver hg38 ./humandb >intervar_20180118.log 2>intervar_20180118.38.err

./annotate_variation.pl -downdb -webfrom annovar ensGene41 --buildver hg38 ./humandb >ensGene41.log 2>ensGene41.err
./annotate_variation.pl -downdb -webfrom annovar dbnsfp42c --buildver hg38 ./humandb >dbnsfp42c.log 2>dbnsfp42c.err
./annotate_variation.pl -downdb -webfrom annovar exac03 --buildver hg38 ./humandb >ensGene41.log 2>ensGene41.err
./annotate_variation.pl -downdb -webfrom annovar  gnomad41_exome --buildver hg38 ./humandb >ensGene41.38.log 2>ensGene41.38.err
./annotate_variation.pl -downdb -webfrom annovar  gnomad41_genome --buildver hg38 ./humandb >gnomad41_genome.38.log 2>gnomad41_genome.38.err
./annotate_variation.pl -downdb -webfrom annovar  dbscsnv11 --buildver hg38 ./humandb >dbscsnv11.38.log 2>dbscsnv11.38.err
./annotate_variation.pl -downdb -webfrom annovar  ljb26_all --buildver hg38 ./humandb >ljb26_all.38.log 2>ljb26_all.38.err
./annotate_variation.pl -downdb -webfrom annovar  revel --buildver hg38 ./humandb >revel.38.log 2>revel.38.err

./annotate_variation.pl -downdb -webfrom annovar  dbnsfp47a_interpro --buildver hg38 ./humandb >dbnsfp47a_interpro.38.log 2>dbnsfp47a_interpro.38.err

#dbnsfp42c,dbnsfp47a_interpro

./annotate_variation.pl -downdb rmsk --buildver hg38 ./humandb >rmsk.38.log 2>rmsk.38.err
# This rmsk annotation source is required by InterVar.
#https://github.com/WGLab/doc-ANNOVAR/issues/201
