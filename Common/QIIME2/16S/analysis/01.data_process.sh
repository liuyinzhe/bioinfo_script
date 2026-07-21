export PATH=/home/Public/software/binary:$PATH
source /home/Public/pipeline/conda_initialize.sh


conda activate  /home/Public/envs/qiime2
export R_HOME=/home/Public/software/miniconda3/envs/qiime2/lib/R
work_dir=/home/Public/project/16S/test
cd ${work_dir}/01.data_process
#import
qiime tools import \
    --type 'SampleData[PairedEndSequencesWithQuality]' \
    --input-path ${work_dir}/data/manifest.tsv \
    --output-path Paired-end.qza \
    --input-format PairedEndFastqManifestPhred33V2 && \
#cutadapt
qiime cutadapt trim-paired \
--i-demultiplexed-sequences Paired-end.qza \
--p-front-f CCTAYGGGRBGCASCAG \
--p-front-r GGACTACNNGGGTATCTAAT  \
--o-trimmed-sequences paired-end-trim.qza \
--verbose >primer_trimming.log && \
#summarize
qiime demux summarize \
     --i-data paired-end-trim.qza \
     --o-visualization paired-demux-summarize.qzv  && \
# denoise
qiime dada2 denoise-paired \
    --i-demultiplexed-seqs paired-end-trim.qza \
    --p-trim-left-f 23 \
    --p-trim-left-r 19 \
    --p-trunc-len-f 0 \
    --p-trunc-len-r 0 \
    --p-n-threads 10 \
    --o-table table.qza \
    --o-representative-sequences rep-seqs.qza \
    --o-denoising-stats denoising-stats.qza \
    --o-base-transition-stats base-transition-stats.qza >denoise.log && \
# summary feature table
 qiime feature-table summarize \
        --i-table table.qza \
        --o-feature-frequencies feature-frequencies.qza \
        --o-sample-frequencies sample-frequencies.qza \
        --o-summary visual-summary.qzv \
        --m-metadata-file ${work_dir}/data/sample-metadata.tsv
conda deactivate
