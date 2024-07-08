/data/software/miniconda3/bin/cutadapt  \
-a GCATGCCCTGCCCCTAAGAATTCG \
-a ACATCTATATCACTATCCCGAACC \
--error-rate 0 \
--overlap  9 \
--no-indels \
--revcomp \
--action lowercase  \
--info-file=reads.adapter.txt \
--output trimmed.fastq \
--cores 2 \
 10.1.fq.gz  

 # Paired-end options:
 #  The -A/-G/-B/-U/-Q options work like their lowercase counterparts, but are applied to R2 (second
 #  read in pair)

 #  -A ADAPTER            3' adapter to be removed from R2
 #  -G ADAPTER            5' adapter to be removed from R2
 #  -B ADAPTER            5'/3 adapter to be removed from R2
 #  -U LENGTH             Remove LENGTH bases from R2

  # -j CORES, --cores CORES
  #                       Number of CPU cores to use. Use 0 to auto-detect. Default: 1
                        
  # -e E, --error-rate E, --errors E
  #                       Maximum allowed error rate (if 0 <= E < 1), or absolute number of errors for
  #                       full-length adapter match (if E is an integer >= 1). Error rate = no. of errors
  #                       divided by length of matching region. Default: 0.1 (10%)
  # --no-indels           Allow only mismatches in alignments. Default: allow both mismatches and indels
  
  # -O MINLENGTH, --overlap MINLENGTH
  #                       Require MINLENGTH overlap between read and adapter for an adapter to be found.
  #                       Default: 3
                        
  # --quality-base N      Assume that quality values in FASTQ are encoded as ascii(quality + N). This
  #                       needs to be set to 64 for some old Illumina FASTQ files. Default: 33
  # --poly-a              Trim poly-A tails

  #   --action {trim,retain,mask,lowercase,crop,none}
  #                       What to do if a match was found. trim: trim adapter and up- or downstream
  #                       sequence; retain: trim, but retain adapter; mask: replace with 'N' characters;
  #                       lowercase: convert to lowercase; crop: trim up and downstream sequence; none:
  #                       leave unchanged. Default: trim
  # --rc, --revcomp       Check both the read and its reverse complement for adapter matches. If match is
  #                       on reverse-complemented version, output that one. Default: check only read
