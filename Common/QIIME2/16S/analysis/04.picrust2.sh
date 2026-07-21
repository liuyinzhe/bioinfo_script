export PATH=/home/Public/software/binary:$PATH
source /home/Public/pipeline/conda_initialize.sh

conda activate  /home/Public/envs/picrust2

# export R_HOME=/home/Public/software/miniconda3/envs/qiime2/lib/R
work_dir=/home/Public/project/16S/test
# silva_database="/home/Public/databases/qiime2/16S/silva-138.1-ssu-nr99-classifier.qza"
cd ${work_dir}/04.picrust2

picrust2_pipeline.py \
   --study_fasta ${work_dir}/02.taxonomic_annotation/final_result/dna-sequences.fasta \
   --input ${work_dir}/02.taxonomic_annotation/final_result/feature-table.biom \
   --output ${work_dir}/04.picrust2/result \
   --processes 10

conda deactivate


#  --in_traits IN_TRAITS
#                        Comma-delimited list (with no spaces) of which gene families to predict from this set: EC, KO, GO, PFAM, BIGG, CAZY, GENE_NAMES.
#                        Note that EC numbers will always be predicted unless --no_pathways is set (default: EC,KO).
