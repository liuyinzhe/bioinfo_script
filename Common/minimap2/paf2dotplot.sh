minimap2 -cx map-hifi 1.bp.p_ctg.fa  lc.fa  > aln.paf

#https://github.com/moold/paf2dotplot
Rscript ./paf2dotplot.r -f -b aln.paf
#Rscript ./paf2dotplot.r -f -b -q 0 -m 0 -r 0  aln.paf
