# assembly
hifiasm related_reads.fasta

# gfa2fasta
awk '/^S/{print ">"$2;print $3}' hifiasm.asm.bp.p_ctg.gfa > hifiasm.L.p_ctg.fa
#gfatools gfa2fa hifiasm.asm.bp.p_ctg.gfa > hifiasm.L.p_ctg.fa
