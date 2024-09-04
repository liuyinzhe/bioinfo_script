
# biom to tsv
biom convert -i otu_table.biom -o otu_table.txt --to-tsv --header-key taxonomy

# tsv to biom
biom convert -i otu_table.txt -o new_otu_table.biom --to-hdf5 --table-type="OTU table" --process-obs-metadata taxonomy

