
#export BAKTA_DB=/data/database/bakta_db/db
#bakta --db <db-path> genome.fasta

export BAKTA_DB=/data/database/bakta_db/db
bakta  genome.fasta \
  --genus GENUS \
  --species SPECIES \
  --strain STRAIN \
  --plasmid PLASMID \
  --threads 8 \
  --tmp-dir $PWD \
  --prefix PREFIX \
  --output OUTPUT \
  --force

#  --db DB, -d DB        Database path (default = <bakta_path>/db). Can also be provided as BAKTA_DB environment variable.
#  --min-contig-length MIN_CONTIG_LENGTH, -m MIN_CONTIG_LENGTH
#                        Minimum contig/sequence size (default = 1; 200 in compliant mode)
#  --force, -f           Force overwriting existing output folder (except for current working directory)
