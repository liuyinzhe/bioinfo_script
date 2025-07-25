python /data/software/annovar/intervar_test/Intervar.modfiy.py \
 -i sample.snp.hg38_multianno.txt \
 --input_type annovar \
 -o sample.snp \
 -b hg38 \
 -t /data/software/annovar/intervardb \
 --table_annovar=/data/software/annovar/table_annovar.pl  \
 --convert2annovar=/data/software/annovar/convert2annovar.pl \
 --annotate_variation=/data/software/annovar/annotate_variation.pl \
 -d /data/software/annovar/humandb
