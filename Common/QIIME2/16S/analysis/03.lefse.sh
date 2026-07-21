export PATH=/home/Public/software/binary:$PATH
source /home/Public/pipeline/conda_initialize.sh

conda activate  /home/Public/envs/lefse

work_dir=/home/Public/project/16S/test
silva_database="/home/Public/databases/qiime2/16S/silva-138.1-ssu-nr99-classifier.qza"
cd ${work_dir}/03.lefse
mkdir -p result
python /home/Public/pipeline/16S/collapse_frequency_table2lefse_input.py \
   -i  ${work_dir}/02.taxonomic_annotation/collapse.frequency.table.tsv \
   -m  ${work_dir}/data/sample-metadata.tsv \
   -o ${work_dir}/03.lefse && \
#collapse.frequency.table.lefse.tsv
#run lefse
# convert text file into lefse.input file 
lefse_format_input.py \
  ${work_dir}/03.lefse/collapse.frequency.table.lefse.tsv \
  ${work_dir}/03.lefse/result/collapse.frequency.table.lefse.in \
  -c 1 \
  -s -1 \
  -u 2 \
  -m f \
  -o 1000000 && \
# run lefse
lefse_run.py \
  ${work_dir}/03.lefse/result/collapse.frequency.table.lefse.in \
  ${work_dir}/03.lefse/result/collapse.frequency.table.lefse.res >${work_dir}/03.lefse/result/lefse.log && \
# select significant result Lefse
grep -E "HTN|Normal" \
    ${work_dir}/03.lefse/result/collapse.frequency.table.lefse.res \
    > ${work_dir}/03.lefse/result/collapse.frequency.table.lefse_signif.res && \
# plot lda 
lefse_plot_res.py \
  ${work_dir}/03.lefse/result/collapse.frequency.table.lefse_signif.res \
  ${work_dir}/03.lefse/result/lefse_final_lda.pdf \
  --format pdf \
  --autoscale 0 && \
lefse_plot_res.py \
  ${work_dir}/03.lefse/result/collapse.frequency.table.lefse_signif.res \
  ${work_dir}/03.lefse/result/lefse_final_lda.png \
  --format png \
  --autoscale 0 && \
# plot cladogram 
lefse_plot_cladogram.py \
  ${work_dir}/03.lefse/result/collapse.frequency.table.lefse_signif.res \
  ${work_dir}/03.lefse/result/lefse_total_clado.pdf \
  --format pdf  && \
lefse_plot_cladogram.py \
  ${work_dir}/03.lefse/result/collapse.frequency.table.lefse_signif.res \
  ${work_dir}/03.lefse/result/lefse_total_clado.png \
  --format png

conda deactivate


