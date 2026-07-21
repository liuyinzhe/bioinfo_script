export PATH=/home/Public/software/binary:$PATH
source /home/Public/pipeline/conda_initialize.sh

conda activate  /home/Public/envs/qiime2

export R_HOME=/home/Public/software/miniconda3/envs/qiime2/lib/R
work_dir=/home/Public/project/16S/test
silva_database="/home/Public/databases/qiime2/16S/silva-138.1-ssu-nr99-classifier.qza"
cd ${work_dir}/02.taxonomic_annotation

qiime feature-classifier classify-sklearn \
                --i-classifier ${silva_database}  \
                --i-reads ${work_dir}/01.data_process/rep-seqs.qza \
                --o-classification ${work_dir}/02.taxonomic_annotation/taxonomy-dada2-sliva.qza \
                --p-n-jobs 20 \
                --verbose && \
# qiime feature-table tabulate-seqs \
#    --i-data ${work_dir}/01.data_process/rep-seqs.qza \
#    --o-visualization ${work_dir}/01.data_process/rep-seqs.qzv
#02.taxonomic_annotation
#step1: remove low occurrence ASVs
qiime feature-table filter-features \
   --i-table ${work_dir}/01.data_process/table.qza \
   --p-min-frequency 10 \
   --p-min-samples 1 \
   --o-filtered-table ${work_dir}/02.taxonomic_annotation/table_filter_low_freq.qza && \
#step2: remove contamination and mitochondria, chloroplast sequence.
qiime taxa filter-table \
   --i-table ${work_dir}/02.taxonomic_annotation/table_filter_low_freq.qza \
   --i-taxonomy  ${work_dir}/02.taxonomic_annotation/taxonomy-dada2-sliva.qza \
   --p-exclude mitochondria,chloroplast \
   --o-filtered-table   ${work_dir}/02.taxonomic_annotation/table_filter_low_freq_contam.qza && \
#step3: drop the low depth samples
# summarise all the ASV counts in each sample
qiime feature-table summarize \
   --i-table ${work_dir}/02.taxonomic_annotation/table_filter_low_freq_contam.qza \
   --o-feature-frequencies feature-frequencies.qza \
   --o-sample-frequencies sample-frequencies.qza \
   --o-summary ${work_dir}/02.taxonomic_annotation/table_filter_low_freq_contam_summary.qzv \
   --verbose && \
# remove samples
qiime feature-table filter-samples \
   --i-table  ${work_dir}/02.taxonomic_annotation/table_filter_low_freq_contam.qza \
   --p-min-frequency 1000 \
   --o-filtered-table  ${work_dir}/02.taxonomic_annotation/final_table.qza && \
# representative sequence
qiime feature-table filter-seqs \
   --i-data ${work_dir}/01.data_process/rep-seqs.qza \
   --i-table ${work_dir}/02.taxonomic_annotation/final_table.qza \
   --o-filtered-data ${work_dir}/02.taxonomic_annotation/final_rep_seqs.qza && \
# reannotate
qiime feature-classifier classify-sklearn \
   --i-classifier ${silva_database}  \
   --i-reads ${work_dir}/02.taxonomic_annotation/final_rep_seqs.qza \
   --o-classification ${work_dir}/02.taxonomic_annotation/final_taxonomy_sliva.qza \
   --p-n-jobs 20 \
   --verbose && \
#### visualizing taxonomic composition
qiime taxa barplot \
     --i-table ${work_dir}/02.taxonomic_annotation/final_table.qza \
     --i-taxonomy ${work_dir}/02.taxonomic_annotation/final_taxonomy_sliva.qza\
     --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
     --o-visualization ${work_dir}/05.diversity/final_taxa_barplots_sliva.qzv && \
# core features
qiime feature-table core-features \
   --i-table ${work_dir}/02.taxonomic_annotation/final_table.qza \
   --p-min-fraction 0.6 \
   --p-max-fraction 1 \
   --p-steps 11 \
   --o-visualization ${work_dir}/02.taxonomic_annotation/final_table_cores.qzv  && \
# 构建系统发育树;用于多样性分析
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences ${work_dir}/02.taxonomic_annotation/final_rep_seqs.qza \
  --o-alignment aligned_rep_seqs.qza \
  --o-masked-alignment masked_aligned_rep_seqs.qza \
  --o-tree unrooted_tree.qza \
  --o-rooted-tree rooted_tree.qza && \
# rarefication curve
qiime diversity alpha-rarefaction \
     --i-table  ${work_dir}/02.taxonomic_annotation/final_table.qza \
     --i-phylogeny ${work_dir}/02.taxonomic_annotation/rooted_tree.qza \
     --p-max-depth 40000 \
     --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
     --o-visualization p-max-depth-40000-alpha-rarefaction.qzv && \
#collapse the table.gza to the L6 level
qiime taxa collapse \
    --i-table ${work_dir}/02.taxonomic_annotation/final_table.qza \
    --o-collapsed-table ${work_dir}/02.taxonomic_annotation/collapse.table.qza \
    --p-level 7 \
    --i-taxonomy ${work_dir}/02.taxonomic_annotation/final_taxonomy_sliva.qza && \
#calculate relative-frequency for the collapsed table (relative abundance instead of counts)
qiime feature-table relative-frequency \
    --i-table ${work_dir}/02.taxonomic_annotation/collapse.table.qza \
    --o-relative-frequency-table ${work_dir}/02.taxonomic_annotation/collapse.frequency.table.qza && \
#export biom file
qiime tools export \
    --input-path ${work_dir}/02.taxonomic_annotation/collapse.frequency.table.qza \
    --output-path ${work_dir}/02.taxonomic_annotation/
#convert biom to text file
biom convert \
    -i ${work_dir}/02.taxonomic_annotation/feature-table.biom \
    -o ${work_dir}/02.taxonomic_annotation/collapse.frequency.table.tsv \
    --header-key "taxonomy" \
    --to-tsv
conda deactivate

# --p-max-depth一般取final_table.qza文件Frequency per sample的中位数左右
# ${work_dir}/01.data_process/paired-demux-summarize.qzv 放到https://view.qiime2.org/visualization
# 查看Frequency per sample 最小值中位数平均值
