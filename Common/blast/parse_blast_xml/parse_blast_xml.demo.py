from Bio.Blast import NCBIXML
num = 0
with open("primer_ASM2364667v1.xml",mode='rt',encoding='utf-8') as xml:
  blast_records =  NCBIXML.parse(xml)
  for record in blast_records:
    #print(dir(record))
    '''
    ['alignments', 'application', 'blast_cutoff', 'database', 'database_length', 
    'database_letters', 'database_name', 'database_sequences', 'date', 'descriptions', 
    'dropoff_1st_pass', 'effective_database_length', 'effective_hsp_length', 
    'effective_query_length', 'effective_search_space', 'effective_search_space_used', 
    'expect', 'filter', 'frameshift', 'gap_penalties', 'gap_trigger', 'gap_x_dropoff', 
    'gap_x_dropoff_final', 'gapped', 'hsps_gapped', 'hsps_no_gap', 'hsps_prelim_gapped', 
    'hsps_prelim_gapped_attemped', 'ka_params', 'ka_params_gap', 'matrix', 
    'multiple_alignment', 'num_good_extends', 'num_hits', 'num_letters_in_database', 
    'num_seqs_better_e', 'num_sequences', 'num_sequences_in_database', 'posted_date', 
    'query', 'query_id', 'query_length', 'query_letters', 'reference', 'sc_match', 
    'sc_mismatch', 'threshold', 'version', 'window_size']
    '''
    application = record.application # BLASTN # 应用软件
    version = record.version
    database = record.database # 数据库路径 /data/genome/ASM2364667v1/ASM2364667v1

    query_name = record.query # AM1840-R
    query_id = record.query_id  # Query_ID
    query_len = record.query_length
    
    # 软件与数据库
    print("application:",application)
    print("version:",version)
    print("database:",database) 

    # query 信息
    print("query_name:",query_name) # AM1840-R
    print("query_id:",query_id) # Query_ID
    #query_len = record.query_letters  两者相同
    # #Source# self._blast.query_length = self._blast.query_letters
    # print("query_letters:",record.query_letters,query_len) # Record the length of the query (PRIVATE).
    # 
    num += 1
    '''
<Iteration>
  <Iteration_iter-num>7</Iteration_iter-num>
  <Iteration_query-ID>Query_7</Iteration_query-ID>
  <Iteration_query-def>AM102-F</Iteration_query-def>
  <Iteration_query-len>20</Iteration_query-len>
<Iteration_hits>
<Hit>
  <Hit_num>1</Hit_num>
  <Hit_id>gnl|BL_ORD_ID|17</Hit_id>
  <Hit_def>CM042715.1 Avena sativa ecotype Sanfensan chromosome 6D, whole genome shotgun sequence</Hit_def>
  <Hit_accession>17</Hit_accession>
  <Hit_len>293840564</Hit_len>
  <Hit_hsps>
    <Hsp>
      <Hsp_num>1</Hsp_num>
      <Hsp_bit-score>36.1753</Hsp_bit-score>
      <Hsp_score>18</Hsp_score>
      <Hsp_evalue>0.27727</Hsp_evalue>
      <Hsp_query-from>1</Hsp_query-from>
      <Hsp_query-to>18</Hsp_query-to>
      <Hsp_hit-from>179394952</Hsp_hit-from>
      <Hsp_hit-to>179394969</Hsp_hit-to>
      <Hsp_query-frame>1</Hsp_query-frame>
      <Hsp_hit-frame>1</Hsp_hit-frame>
      <Hsp_identity>18</Hsp_identity>
      <Hsp_positive>18</Hsp_positive>
      <Hsp_gaps>0</Hsp_gaps>
      <Hsp_align-len>18</Hsp_align-len>
      <Hsp_qseq>GCCTGACCTTTTTCCGCA</Hsp_qseq>
      <Hsp_hseq>GCCTGACCTTTTTCCGCA</Hsp_hseq>
      <Hsp_midline>||||||||||||||||||</Hsp_midline>
    </Hsp>
    <Hsp>
      <Hsp_num>1</Hsp_num>
      <Hsp_bit-score>32.2105</Hsp_bit-score>
      <Hsp_score>16</Hsp_score>
      <Hsp_evalue>6.49366</Hsp_evalue>
      <Hsp_query-from>1</Hsp_query-from>
      <Hsp_query-to>20</Hsp_query-to>
      <Hsp_hit-from>97774503</Hsp_hit-from>
      <Hsp_hit-to>97774522</Hsp_hit-to>
      <Hsp_query-frame>1</Hsp_query-frame>
      <Hsp_hit-frame>1</Hsp_hit-frame>
      <Hsp_identity>19</Hsp_identity>
      <Hsp_positive>19</Hsp_positive>
      <Hsp_gaps>0</Hsp_gaps>
      <Hsp_align-len>20</Hsp_align-len>
      <Hsp_qseq>CTTCTGCCCATGAAACCCTA</Hsp_qseq>
      <Hsp_hseq>CTTCTTCCCATGAAACCCTA</Hsp_hseq>
      <Hsp_midline>||||| ||||||||||||||</Hsp_midline>
    </Hsp>
  </Hit_hsps>
</Hit>
</Iteration_hits>
  <Iteration_stat>
    <Statistics>
      <Statistics_db-num>134</Statistics_db-num>
      <Statistics_db-len>10757463545</Statistics_db-len>
      <Statistics_hsp-len>16</Statistics_hsp-len>
      <Statistics_eff-space>21514922802</Statistics_eff-space>
      <Statistics_kappa>0.710602795216363</Statistics_kappa>
      <Statistics_lambda>1.37406312246009</Statistics_lambda>
      <Statistics_entropy>1.30724660390929</Statistics_entropy>
    </Statistics>
  </Iteration_stat>
</Iteration>
    '''
    for alignment in record.alignments:
        #print(dir(alignment))
        '''
        ['accession', 'hit_def', 'hit_id', 'hsps', 'length', 'title']
        '''
        hit_ref_id = alignment.hit_id   # gnl|BL_ORD_ID|8
        hit_ref_title = alignment.title # gnl|BL_ORD_ID|8 CM042706.1 Avena sativa ecotype Sanfensan chromosome 3D, whole genome shotgun sequence
        hit_accession = alignment.accession # 数据库访问号 8,"gnl|BL_ORD_ID|8 中的8"
        hit_definition = alignment.hit_def # CM042706.1 Avena sativa ecotype Sanfensan chromosome 3D, whole genome shotgun sequence
        
        hit_ref_chromosome_id = hit_definition.split(" ")[0] # CM042706.1
        hit_ref_length = alignment.length # CM042706.1 chromosome 3D 长度
        print("hit_ref_id:",hit_ref_id)
        print("hit_ref_title",hit_ref_title)
        print("hit_accession:",hit_accession)
        print("hit_definition:",hit_definition)
        print("#"*10,hit_accession,hit_ref_chromosome_id,"#"*10)
        for hsp in alignment.hsps:
            #print(dir(hsp))
            '''
            ['align_length', 'bits', 'expect', 'frame', 'gaps', 
            'identities', 'match', 'num_alignments', 'positives',
            'query', 'query_end', 'query_start', 'sbjct', 'sbjct_end',
            'sbjct_start', 'score', 'strand']
            '''
            # hsp 局部对齐
            hsp_query_sequence = hsp.query
            hsp_match_str = hsp.match
            hsp_sbjct_hit_sequence = hsp.sbjct

            # query alignment position
            hsp_query_start = hsp.query_start
            hsp_query_end = hsp.query_end

            # sbjct alignment position
            hsp_sbjct_start = hsp.sbjct_start
            hsp_sbjct_end = hsp.sbjct_end

            # 方向
            hsp_strand = hsp.strand # ('Plus', 'Plus') ('Plus', 'Minus')
            hsp_frame = hsp.frame # (1,1) (1,-1) #1 表示正向，-1 表示反向 

            # 未知，暂无用处
            hsp_num_alignments = hsp.num_alignments # None
            

            hsp_e_val = hsp.expect # 期望值
            hsp_bits = hsp.bits # 与hsp_score 相关
            hsp_score = hsp.score # 得分,没有gap 就不会掉分

            
            hsp_positives = hsp.positives # hsp匹配的碱基数
            hsp_align_len = hsp.align_length  # 最长跨越长度
            hsp_identities = hsp.identities ## 类似Bam Match包含mismatch,只写了match 长度
            hsp_gaps = hsp.gaps

            # 局部比对情况
            print("match_base:",hsp_positives) # 完全对应的长度
            print("align_len:",hsp_align_len)  # 最长跨越长度
            print("identities:",hsp_identities) # 类似Bam Match包含mismatch

            # 打分
            print("hsp_gaps:",hsp_gaps)
            print("hsp_score:",hsp_score)
            print("hsp_bits:",hsp_bits)
 
            print("hsp_num_alignments:",hsp_num_alignments)

            # 坐标
            print("hsp_query_start:",hsp_query_start)
            print("hsp_query_end:",hsp_query_end)
            print("hsp_sbjct_start:",hsp_sbjct_start)
            print("hsp_sbjct_end:",hsp_sbjct_end)

            # 序列方向
            print("hsp_strand:",hsp_strand)
            print("hsp_frame:",hsp_frame)
            # hsp 局部对齐
            print(hsp_query_sequence)
            print(hsp_match_str)
            print(hsp_sbjct_hit_sequence)
          
