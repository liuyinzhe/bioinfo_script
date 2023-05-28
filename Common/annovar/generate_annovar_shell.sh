VCF_PATH=../05.gatk  # ${sample}.sorted.markdup.bam 
VAR_PATH=${PWD}
REF=/data/database/genome/human_hg19/hg19.fa
gatk=/data/software/envs/Common/bin/gatk
GATK_dbsnp=/data/database/GATK_bundle/hg19/dbsnp_138.hg19.vcf.gz

cd ${VAR_PATH}
rm -rf batch_annovar.sh
while read tumor normal ; do 
sample=$(echo ${tumor}"_"${normal})
mkdir -p ${sample}

echo -e "cd ${VAR_PATH} ; \
/data/software/annovar/table_annovar.pl \
  ${VCF_PATH}/${sample}/${sample}.wes.somatic.PASS.vcf \
  /data/software/annovar/humandb/ \
  -buildver hg19 \
  -out ${sample} \
  -remove \
  -protocol refGene,avsnp150,1000g2015aug_all,1000g2015aug_eas,clinvar_20230520,intervar_20180118,cosmic68,exac03,dbnsfp42c,dbscsnv11,gnomad211_exome,gnomad211_genome,esp6500siv2_all,ljb26_all,revel \
  -operation g,f,f,f,f,f,f,f,f,f,f,f,f,f,f \
  -nastring \. -vcfinput  " >> batch_annovar.sh

done < tumor_normal_pair
