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
