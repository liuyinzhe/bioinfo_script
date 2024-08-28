### 帮助信息
```
    python -m jcvi.formats.blast ACTION

Available ACTIONs:
         anchors | Keep only the BLAST pairs that are in the anchors file
        annotate | Annotate overlap types in BLAST tabular file
      annotation | Create tabular file with the annotations
             bed | Get bed file from BLAST tabular file
            best | Get best BLAST hit per query
           chain | Chain adjacent HSPs together
    completeness | Print completeness statistics for each query
        condense | Group HSPs together for same query-subject pair
       covfilter | Filter BLAST file (based on id% and cov%)
          cscore | Calculate C-score for BLAST pairs
          filter | Filter BLAST file (based on score, id%, alignlen)
            gaps | Find distribution of gap sizes between adjacent HSPs
      mismatches | Print out histogram of mismatches of HSPs
           pairs | Print paired-end reads of BLAST tabular file
            rbbh | Find reciprocal-best blast hits
           score | Add up the scores for each query seq
            sort | Sort lines so that query grouped together and scores desc
          subset | Extract hits from some query and subject chrs
         summary | Provide summary on id% and cov%
            swap | Swap query and subjects in BLAST tabular file
           top10 | Count the most frequent 10 hits
```

### 查找最好比对
```bash
python -m jcvi.formats.blast best result.blast 
```
### 汇总blast
```bash
python -m jcvi.formats.blast summary result.blast 
```
