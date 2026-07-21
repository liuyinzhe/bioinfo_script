#qiime2-amplicon-2024.5 不能读取 2026.4的qiime2 qza数据结构
export PATH=/home/Public/software/binary:$PATH
source /home/Public/pipeline/conda_initialize.sh

conda activate  /home/Public/envs/q2-picrust2-qiime2

export R_HOME=/home/Public/software/miniconda3/envs/qiime2/lib/R
work_dir=/home/Public/project/16S/test
# silva_database="/home/Public/databases/qiime2/16S/silva-138.1-ssu-nr99-classifier.qza"
cd ${work_dir}/04.picrust2

qiime picrust2 full-pipeline \
   --i-table ${work_dir}/02.taxonomic_annotation/final_table.qza \
   --i-seq ${work_dir}/02.taxonomic_annotation/final_rep_seqs.qza \
   --p-placement-tool epa-ng \
   --p-threads 10 \
   --p-hsp-method mp \
   --o-ko-metagenome ko_metagenome.qza \
   --o-ec-metagenome ec_metagenome.qza \
   --o-pathway-abundance pathway_abundance.qza \
   --verbose && \
qiime feature-table summarize \
   --i-table ${work_dir}/04.picrust2/pathway_abundance.qza \
   --o-visualization ${work_dir}/04.picrust2/pathway_abundance.qzv

conda deactivate
