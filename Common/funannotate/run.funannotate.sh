
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
