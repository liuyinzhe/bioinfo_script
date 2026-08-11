
funannotate clean -i scaffold.fa  -o cleaned.fa
funannotate sort --input cleaned.fa --out sorted.fa --minlen 10
funannotate mask --input sorted.fa  --out masked.fa


funannotate predict \
   -i masked.fa \
   --species "AAAA bbbb" \
   --name  "AoFC_" \
   --rna_bam alignments.bam \
   --out output
#   --isolate "isolate_name" \
#   --strain "strain_name" \
#   --transcript_evidence trinity.fasta \
#   --pasa_gff pasa.gff3

#################

conda activate /data/users/liuyz/envs/funannotate
export FUNANNOTATE_DB=/data/database/funannotate_db
export GENEMARK_PATH=/data/software/GeneMark/gmes_linux_64_4
funannotate predict \
   -i masked.fa \
   --species "Aspergillus westerdijkiae" \
   --name  "AoFC_" \
   --rna_bam /data/project/funannotate/04.predict/ABC/ABC.sorted.bam \
   --out output
#   --isolate "isolate_name" \
#   --strain "strain_name" \
#   --transcript_evidence trinity.fasta \
#   --pasa_gff pasa.gff3

conda deactivate
