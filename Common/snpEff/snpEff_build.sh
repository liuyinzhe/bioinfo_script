# Databases & Genomes
cd ~/software/snpEff
echo -e "# HPA_v1\nHPA_v1.genome : HPA" >>snpEff.config

mkdir -p ~/software/snpEff/data/HPA_v1
cp -a genes.gff  sequences.fa  ~/software/snpEff/data/HPA_v1
gffread genes.gff -g sequences.fa -y protein.fa
gffread genes.gff -g sequences.fa -x cds.fa
# -noCheckCds -noCheckProtein 非必须 cds.fa protein.fa 
# 不加 -noCheckCds -noCheckProtein ,建库会失败
java -jar ~/software/snpEff/snpEff.jar build -gff3 -v HPA_v1 -d -noCheckCds -noCheckProtein

java -jar ~/software/snpEff/snpEff.jar ann HPA input.vcf.gz > snpeff.vcf
