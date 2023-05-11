while read sampleA sampleB ; do 

echo -e "#!/bin/bash 
cd  ${PWD}
PATH=/software/miniconda3/bin:$PATH; \\
featureCounts \\
  -Q 50 \\
  --primary \\
  --ignoreDup \\
  --nonSplitOnly \\
  -T 2 \\
  -p \\
  -t CDS \\
  -g gene_id \\
  -a /data/database/genome/ref.gtf \\
  -o all.counts.${sampleA}_vs_${sampleB}.txt \\
   ${sampleA}.sorted.bam \\
   ${sampleB}.sorted.bam" > featureCounts_${sampleA}_vs_${sampleB}.sh


done < pair_lst

ls  featureCounts_*.sh | xargs -i echo sh {} > run.sh
