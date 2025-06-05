cat *.fasta > all.fa
mafft  --auto --phylipout --reorder all.fa > all.phy
iqtree -s all.phy -T 20
