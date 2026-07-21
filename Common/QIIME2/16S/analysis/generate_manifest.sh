work_dir=/home/Public/project/16S/test/
python /home/Public/pipeline/16S/generate_manifest.py \
	 -m ${work_dir}/data/sample-metadata.tsv \
	 -d ${work_dir}/data \
	 -o ${work_dir}/data/manifest.tsv
