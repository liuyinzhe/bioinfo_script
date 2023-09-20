import gzip
import re
import sys
import copy
import time
import datetime
'''
input :result.blast
# 获取 每个target_seq 的最佳 目标序列ID
# 有用信息预先构造
#
qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovs qcovhsp qcovus

xx      KX610138.1      99.462  558     0       3       567     3       558     828     824     268     0.0     1011    98      98      98
qseqid* sseqid* pident* length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovs* qcovhsp qcovus tax

# 预先读取文件存入内存
# /data/home/liuyinzhe/database/taxonomy/tax_id2name.txt

# 单独读取，读取过程中进行查询是否在字典内
# /data/home/liuyinzhe/database/taxonomy/dead_nucl.accession2taxid.gz
# # 逐步减少列表，保存对应id 序列，用于后续输出

# 根据id序列输出
# 输出readme 序列 
'''


def main():
    # 说明
    readme_str = '''

    qseqid* sseqid* pident* length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovs* qcovhsp qcovus latin_name* genus_name*

    结果中主要看这几个字段 qseqid* sseqid* pident* qcovs* latin_name* genus_name*
    字段 qcovs 作为Coverage , pident 作为 identity 理解

    blast++ 常见字段含义：
                qseqid means Query Seq-id
                qgi means Query GI
                qacc means Query accesion
            qaccver means Query accesion.version
                qlen means Query sequence length
                sseqid means Subject Seq-id
            sallseqid means All subject Seq-id(s), separated by a ';'
                sgi means Subject GI
                sallgi means All subject GIs
                sacc means Subject accession
            saccver means Subject accession.version
            sallacc means All subject accessions
                slen means Subject sequence length
                qstart means Start of alignment in query
                qend means End of alignment in query
                sstart means Start of alignment in subject
                send means End of alignment in subject
                qseq means Aligned part of query sequence
                sseq means Aligned part of subject sequence
                evalue means Expect value
            bitscore means Bit score
                score means Raw score
                length means Alignment length
                pident means Percentage of identical matches
                nident means Number of identical matches
            mismatch means Number of mismatches
            positive means Number of positive-scoring matches
            gapopen means Number of gap openings
                gaps means Total number of gaps
                ppos means Percentage of positive-scoring matches
                frames means Query and subject frames separated by a '/'
                qframe means Query frame
                sframe means Subject frame
                btop means Blast traceback operations (BTOP)
                staxid means Subject Taxonomy ID
            ssciname means Subject Scientific Name
            scomname means Subject Common Name
            sblastname means Subject Blast Name
            sskingdom means Subject Super Kingdom
            staxids means unique Subject Taxonomy ID(s), separated by a ';'
                            (in numerical order)
            sscinames means unique Subject Scientific Name(s), separated by a ';'
            scomnames means unique Subject Common Name(s), separated by a ';'
            sblastnames means unique Subject Blast Name(s), separated by a ';'
                            (in alphabetical order)
            sskingdoms means unique Subject Super Kingdom(s), separated by a ';'
                            (in alphabetical order) 
                stitle means Subject Title
            salltitles means All Subject Title(s), separated by a '<>'
            sstrand means Subject Strand
                qcovs means Query Coverage Per Subject
            qcovhsp means Query Coverage Per HSP
                qcovus means Query Coverage Per Unique Subject (blastn only)
    '''
    qseqid_lst = []
    sseqid_lst = []
    best_hit_dic = {}
    with open("result.blast",mode='rt',encoding='utf-8') as fh:
        for line in fh:
            record = re.split('\t',line.strip())
            '''
            qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovs qcovhsp qcovus
            0001_32823081101514_(2034)_[ITS1]       LT626976.1      99.459  555     0       3       577     22      574     814     85      638     0.0     1005    96      96      96
            '''
            qseqid = record[0]
            sseq_id = record[1]
            if qseqid not in best_hit_dic:
                best_hit_dic[qseqid] = record
                sseqid_lst.append(sseq_id)
                qseqid_lst.append(qseqid)
    taxonomy_dic = {} # id:[拉丁全称,属名]
    with open("/data/home/liuyinzhe/database/taxonomy/tax_id2name.txt",mode='rt',encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('taxonomy_id'):
                continue
            
            record = re.split('\t',line.strip('\n'))#.strip())
            #print(record)
            taxonomy_id = record[0]
            Kingdom_name = record[1]
            Phylum_name = record[2]
            Family_name = record[3]
            Genus_name = record[4]
            latin_name = record[5]
            if latin_name.startswith('uncultured'):
                Genus_name = re.split('\s+',latin_name)[1]
            else:
                Genus_name = re.split('\s+',latin_name)[0]

            if taxonomy_id not in taxonomy_dic:
                taxonomy_dic[taxonomy_id] = [Kingdom_name,Phylum_name,Family_name,Genus_name,latin_name]

    sseqid_tmp = set(copy.copy(sseqid_lst))
    accession2taxid_dic = {}
    print(len(sseqid_tmp))
    with gzip.open('/data/home/liuyinzhe/database/taxonomy/nucl_gb.accession2taxid.gz',mode='rt') as gz, \
        open('result.xls',mode='wt',encoding='utf-8') as out,open('table_header_readme.txt',mode='wt',encoding='utf-8') as readme,\
        open('acc2taxid.xls',mode='wt',encoding='utf-8') as lst_obj,\
        open('unknow_blast.xls',mode='wt',encoding='utf-8') as unknow:
        blast_header = "qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqlen\tqstart\tqend\tslen\tsstart\tsend\tevalue\tbitscore\tqcovs\tqcovhsp\tqcovus\n"
        unknow.write(blast_header)
        for line in gz:
            '''
            accession       accession.version       taxid   gi
            A00001          A00001.1               10641   58418
            '''
            record = re.split('\t',str(line).strip())
            accver = record[1]
            taxid = record[2]
            #print(taxid,accver)
            if len(sseqid_tmp) != 0 and accver in sseqid_tmp:
                print(accver,taxid,'bingo')
                sseqid_tmp.remove(accver)
                #print(len(sseqid_tmp))
                accession2taxid_dic[accver] = taxid
            elif len(sseqid_tmp) == 0:
                break
            else:
                continue
        print(sseqid_tmp)
        print(len(sseqid_tmp))

        # 开始 写
        readme.write(readme_str)
        #
        header_str = "qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqlen\tqstart\tqend\tslen\tsstart\tsend\tevalue\tbitscore\tqcovs\tqcovhsp\tqcovus\tKingdom_name\tPhylum_name\tFamily_name\tGenus_name\tlatin_name\n"
        out.write(header_str)
        for index in range(len(sseqid_lst)):
            sseqid = sseqid_lst[index] # subject
            qseqid = qseqid_lst[index] # query
            record_lst = best_hit_dic[qseqid]
            #accession2taxid_dic[accver]=taxid
            #taxonomy_dic[taxonomy_id] = [latin_name,genus_name]
            if sseqid not in  accession2taxid_dic:
                unknow.write('\t'.join(best_hit_dic[qseqid])+'\n')
                continue
            taxonomy_id = accession2taxid_dic[sseqid]
            Kingdom_name,Phylum_name,Family_name,Genus_name,latin_name = taxonomy_dic[taxonomy_id]
            lst_obj.write('\t'.join([sseqid,taxonomy_id,Kingdom_name,Phylum_name,Family_name,Genus_name,latin_name])+'\n')
            # record_lst.append(latin_name)
            # record_lst.append(genus_name)
            record_lst += taxonomy_dic[accession2taxid_dic[sseqid]]
            out.write('\t'.join(record_lst)+'\n')


if __name__ == "__main__":
    if sys.version[0] == "3":
        start_time = time.perf_counter()
    else:
        start_time = time.clock()
    main()
    if sys.version[0] == "3":
        end_time = time.perf_counter()
    else:
        end_time = time.clock()
    print("%s %s %s\n" % ("main()", "use", str(
        datetime.timedelta(seconds=end_time - start_time))))
