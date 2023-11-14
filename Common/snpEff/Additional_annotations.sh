


java -Xmx8g -jar ~/software/snpEff/snpEff.jar -o vcf -geneId -hgvs -hgvsTrId -lof   hg38 Sample.indel.filter.vcf.gz > new.vcf
java -Xmx8g -jar ~/software/snpEff/snpEff.jar -o gatk -geneId  -hgvs -hgvsTrId    hg38 Sample.indel.filter.vcf.gz >new.gatk.vcf
java -Xmx8g -jar ~/software/snpEff/snpEff.jar -o bed -geneId  -hgvs -hgvsTrId    hg38 Sample.indel.filter.vcf.gz >new.bed
java -Xmx8g -jar ~/software/snpEff/snpEff.jar -o bedann -geneId  -hgvs -hgvsTrId    hg38 Sample.indel.filter.vcf.gz >new.bedann


java -Xmx8g -jar ~/software/snpEff/snpEff.jar -o vcf -geneId -hgvs -hgvsTrId -lof hg38 Sample.snp.filter.vcf.gz > new.snp.vcf
java -Xmx8g -jar ~/software/snpEff/snpEff.jar -o vcf -geneId -hgvsOld -hgvsTrId -hgvs1LetterAa -lof hg38 Sample.snp.filter.vcf.gz > new.snp.old.vcf


## Using the -cancer command line option, you can compare somatic vs germline samples.
java -Xmx8g -jar snpEff.jar -v -cancer GRCh37.75 cancer.vcf > cancer.ann.vcf
