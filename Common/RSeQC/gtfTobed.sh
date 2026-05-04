#conda search ucsc-gtftogenepred  
#wget -c http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/genePredToBed
#wget -c http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/gtfToGenePred

binary=/software/ucsc_bin
$binary/gtfToGenePred hg38.refGene.gtf hg38.ensembl.genePred
$binary/genePredToBed hg38.ensembl.genePred hg38.ensembl.bed
