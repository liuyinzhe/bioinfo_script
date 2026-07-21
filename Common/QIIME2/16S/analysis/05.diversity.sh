
export PATH=/home/Public/software/binary:$PATH
source /home/Public/pipeline/conda_initialize.sh

conda activate  /home/Public/envs/qiime2

export R_HOME=/home/Public/software/miniconda3/envs/qiime2/lib/R
work_dir=/home/Public/project/16S/test
# silva_database="/home/Public/databases/qiime2/16S/silva-138.1-ssu-nr99-classifier.qza"

sampling_depth=10000
cd ${work_dir}/05.diversity


# all diversity index and distance
qiime diversity core-metrics-phylogenetic \
     --i-phylogeny ${work_dir}/02.taxonomic_annotation/rooted_tree.qza \
     --i-table ${work_dir}/02.taxonomic_annotation/final_table.qza \
     --p-sampling-depth ${sampling_depth} \
     --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
     --output-dir sample-depth-${sampling_depth}-core-metrics-results && \
# rarefied_table.qza                      #The resulting rarefied feature table.        
# faith_pd_vector.qza                     #Vector of Faith PD values by sample.
# shannon_vector.qza                      #Vector of Shannon diversity values by sample.
# evenness_vector.qza                     #Vector of Pielou's evenness values by sample.
# observed_features_vector.qza            #Vector of Observed Features values by sample.
# bray_curtis_distance_matrix.qza         #Matrix of Bray-Curtis distances between pairs of samples.
# bray_curtis_emperor.qzv                 #Emperor plot of the PCoA matrix computed from Bray-Curtis.
# bray_curtis_pcoa_results.qza            #PCoA matrix computed from Bray-Curtis distances between samples.
# jaccard_distance_matrix.qza             #Matrix of Jaccard distances between pairs of samples.
# jaccard_emperor.qzv                     #Emperor plot of the PCoA matrix computed from Jaccard.
# jaccard_pcoa_results.qza                #PCoA matrix computed from Jaccard distances between samples.
# weighted_unifrac_distance_matrix.qza    #Matrix of weighted UniFrac distances between pairsof samples.
# unweighted_unifrac_distance_matrix.qza  #Matrix of unweighted UniFrac distances between pairs of samples.
# weighted_unifrac_emperor.qzv            #Emperor plot of the PCoA matrix computed from weighted UniFrac.
# unweighted_unifrac_emperor.qzv          #Emperor plot of the PCoA matrix computed from unweighted UniFrac.
# weighted_unifrac_pcoa_results.qza       #PCoA matrix computed from weighted UniFrac distances between samples.
# unweighted_unifrac_pcoa_results.qza     #PCoA matrix computed from unweighted UniFrac distances between samples.
#### faith_pd diversity parameters
# example for faith_pd_vector of group analysis
qiime diversity alpha-group-significance \
     --i-alpha-diversity ${work_dir}/05.diversity/sample-depth-${sampling_depth}-core-metrics-results/faith_pd_vector.qza \
     --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
     --o-visualization ${work_dir}/05.diversity/sample-depth-${sampling_depth}-core-metrics-results/faith-pd-group-significance.qzv && \
# example for alpha diversity of group analysis
qiime diversity alpha-group-significance \
     --i-alpha-diversity ${work_dir}/05.diversity/sample-depth-${sampling_depth}-core-metrics-results/shannon_vector.qza \
     --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
     --o-visualization ${work_dir}/05.diversity/shannon_compare_groups.qzv && \
# beta diversity 
qiime diversity beta-group-significance \
    --i-distance-matrix ${work_dir}/05.diversity/sample-depth-${sampling_depth}-core-metrics-results/unweighted_unifrac_distance_matrix.qza \
    --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
    --m-metadata-column Treatment \
    --p-pairwise false \
    --p-permutations 999 \
    --o-visualization ${work_dir}/05.diversity/unweighted-unifrac-subject-significance.qzv && \
# three dimensions to show beta diversity
qiime emperor plot \
    --i-pcoa ${work_dir}/05.diversity/sample-depth-${sampling_depth}-core-metrics-results/unweighted_unifrac_pcoa_results.qza \
    --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
    --p-custom-axes Treatment \
    --o-visualization ${work_dir}/05.diversity/unweighted-unifrac-emperor-height.qzv && \
#### Analysis of composition of microbiomes (ANCOM)
# add pseudocount for log transform
qiime composition add-pseudocount \
   --i-table ${work_dir}/02.taxonomic_annotation/final_table.qza \
   --p-pseudocount 1 \
   --o-composition-table ${work_dir}/05.diversity/final_table_pseudocount.qza && \
# ANCOM 
qiime composition ancom \
   --i-table ${work_dir}/05.diversity/final_table_pseudocount.qza \
   --m-metadata-file ${work_dir}/data/sample-metadata.tsv \
   --m-metadata-column Treatment \
   --output-dir ${work_dir}/05.diversity/ancom_output

conda deactivate

