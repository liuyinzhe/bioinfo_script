


# call 参数

--base-quality-score-threshold <Byte>
                              Base qualities below this threshold will be reduced to the minimum (6)  Default value: 18.

# call 变异的最低深度
--callable-depth <Integer>    Minimum depth to be considered callable for Mutect stats.  Does not affect genotyping. 
                              Default value: 10. 


# 其它参数

--tmp-dir <GATKPath>          Temp directory to use.  Default value: null. 


# 索引与md5
--create-output-bam-index,-OBI <Boolean>
                              If true, create a BAM/CRAM index when writing a coordinate-sorted BAM/CRAM file.  Default
                              value: true. Possible values: {true, false} 

--create-output-bam-md5,-OBM <Boolean>
                              If true, create a MD5 digest for any BAM/SAM/CRAM file created  Default value: false.
                              Possible values: {true, false} 


--create-output-variant-index,-OVI <Boolean>
                              If true, create a VCF index when writing a coordinate-sorted VCF file.  Default value:
                              true. Possible values: {true, false} 

--create-output-variant-md5,-OVM <Boolean>
                              If true, create a a MD5 digest any VCF file created.  Default value: false. Possible
                              values: {true, false} 


#  关闭特征筛选 过滤


--disable-read-filter,-DF <String>
                              Read filters to be disabled before analysis  This argument may be specified 0 or more
                              times. Default value: null. Possible values: {GoodCigarReadFilter, MappedReadFilter,
                              MappingQualityAvailableReadFilter, MappingQualityNotZeroReadFilter,
                              MappingQualityReadFilter, NonChimericOriginalAlignmentReadFilter,
                              NonZeroReferenceLengthAlignmentReadFilter, NotDuplicateReadFilter,
                              NotSecondaryAlignmentReadFilter, PassesVendorQualityCheckReadFilter, ReadLengthReadFilter,
                              WellformedReadFilterPossible values: {



--dont-use-dragstr-pair-hmm-scores <Boolean>
                              disable DRAGstr pair-hmm score even when dragstr-params-path was provided  Default value:
                              false. Possible values: {true, false} 

--enable-dynamic-read-disqualification-for-genotyping <Boolean>
                              Will enable less strict read disqualification low base quality reads  Default value:
                              false. Possible values: {true, false} 



# 排除区域
--exclude-intervals,-XL <String>
                              One or more genomic intervals to exclude from processing  This argument may be specified 0
                              or more times. Default value: null. 


# 深度，分组grouped
--f1r2-max-depth <Integer>    sites with depth higher than this value will be grouped  Default value: 200. 
# 比对质量中位数
--f1r2-median-mq <Integer>    skip sites with median mapping quality below this value  Default value: 50. 

#  pileup  过滤质量
--f1r2-min-bq <Integer>       exclude bases below this quality from pileup  Default value: 20. 





# 外部
--germline-resource <FeatureInput>
                              Population vcf of germline sequencing containing allele fractions.  Default value: null. 

# debug log
--graph-output,-graph <String>Write debug assembly graph information to this file  Default value: null. 

--debug-assembly,-debug <Boolean>
                              Print out verbose debug information about each assembly region  Default value: false.
                              Possible values: {true, false} 


# 区间
--intervals,-L <String>       One or more genomic intervals over which to operate  This argument may be specified 0 or
                              more times. Default value: null. 

# 最大组装区域的大小
--max-assembly-region-size <Integer>
                              Maximum size of an assembly region  Default value: 300. 

# 最大群体AF 0.01  在 tumor-only mode
--max-population-af,-max-af <Double>
                              Maximum population allele frequency in tumor-only mode.  Default value: 0.01. 

--max-reads-per-alignment-start <Integer>
                              Maximum number of reads to retain per alignment start position. Reads above this threshold
                              will be downsampled. Set to 0 to disable.  Default value: 50. 

--max-variants-per-shard <Integer>
                              If non-zero, partitions VCF output into shards, each containing up to the given number of
                              records.  Default value: 0. 
# 最小组装区域大小
--min-assembly-region-size <Integer>
                              Minimum size of an assembly region  Default value: 50. 
# 最小call变异的碱基质量 10
--min-base-quality-score,-mbq <Byte>
                              Minimum base quality required to consider a base for calling  Default value: 10. 


--native-pair-hmm-threads <Integer>
                              How many threads should a native pairHMM implementation use  Default value: 4. 

--native-pair-hmm-use-double-precision <Boolean>
                              use double precision in the native pairHmm. This is slower but matches the java
                              implementation better  Default value: false. Possible values: {true, false} 

--normal-sample,-normal <String>
                              BAM sample name of normal(s), if any.  May be URL-encoded as output by GetSampleName with
                              -encode argument.  This argument may be specified 0 or more times. Default value: null. 




# ##########################################
Advanced Arguments:

--active-probability-threshold <Double>
                              Minimum probability for a locus to be considered active.  Default value: 0.002. 

--adaptive-pruning-initial-error-rate <Double>
                              Initial base error rate estimate for adaptive pruning  Default value: 0.001. 

--allele-informative-reads-overlap-margin <Integer>
                              Likelihood and read-based annotations will only take into consideration reads that overlap
                              the variant or any base no further than this distance expressed in base pairs  Default
                              value: 2. 

--kmer-size <Integer>         Kmer size to use in the read threading assembler  This argument may be specified 0 or more
                              times. Default value: [10, 25]. 

--likelihood-calculation-engine <Implementation>
                              What likelihood calculation engine to use to calculate the relative likelihood of reads vs
                              haplotypes  Default value: PairHMM. Possible values: {PairHMM, FlowBased, FlowBasedHMM} 

--linked-de-bruijn-graph <Boolean>
                              If enabled, the Assembly Engine will construct a Linked De Bruijn graph to recover better
                              haplotypes  Default value: false. Possible values: {true, false} 

# 最大 MNP 中多出来的碱基数量
--max-mnp-distance,-mnp-dist <Integer>
                              Two or more phased substitutions separated by this distance or less are merged into MNPs. 
                              Default value: 1. 

--max-num-haplotypes-in-population <Integer>
                              Maximum number of haplotypes to consider for your population  Default value: 128. 


--min-pruning <Integer>       Minimum support to not prune paths in the graph  Default value: 2. 

--num-pruning-samples <Integer>
                              Number of samples that must pass the minPruning threshold  Default value: 1. 

--pair-hmm-gap-continuation-penalty <Integer>
                              Flat gap continuation penalty for use in the Pair HMM  Default value: 10. 

--pair-hmm-implementation,-pairHMM <Implementation>
                              The PairHMM implementation to use for genotype likelihood calculations  Default value:
                              FASTEST_AVAILABLE. Possible values: {EXACT, ORIGINAL, LOGLESS_CACHING,
                              AVX_LOGLESS_CACHING, AVX_LOGLESS_CACHING_OMP, FASTEST_AVAILABLE} 



--showHidden <Boolean>        display hidden arguments  Default value: false. Possible values: {true, false} 


Conditional Arguments for readFilter:

Valid only if "MappingQualityReadFilter" is specified:
--maximum-mapping-quality <Integer>
                              Maximum mapping quality to keep (inclusive)  Default value: null. 

--minimum-mapping-quality <Integer>
                              Minimum mapping quality to keep (inclusive)  Default value: 20. 

Valid only if "ReadLengthReadFilter" is specified:
--max-read-length <Integer>   Keep only reads with length at most equal to the specified value  Default value:
                              2147483647. 
#  最小 reads 长度
--min-read-length <Integer>   Keep only reads with length at least equal to the specified value  Default value: 30. 


***********************************************************************
