import gzip
import re
import sys
import copy
import time
import datetime

'''
taxon_lineage.tsv  to tax_id2name.txt
'''

def main():

    '''
    taxon_id    界 Kingdom      门 Phylum       纲 Class            目 Order                科 Family               属 Genus                        种 Species
    0               1           2               3              4                    5                       6                               7
    11560       Viruses     Negarnaviricota Insthoviricetes Articulavirales     Orthomyxoviridae        Gammainfluenzavirus     Gammainfluenzavirus influenzae
    
    '''
    taxonomy_dic = {} # id:[拉丁全称,属名]
    with open("taxon_lineage.tsv",mode='rt',encoding='utf-8') as fh,open('tax_id2name.txt',mode='wt',encoding='utf-8') as out:
        out.write("taxonomy_id\tKingdom_name\tPhylum_name\tFamily_name\tGenus_name\tlatin_name\n")
        for line in fh:
            record = re.split('\t',line.strip('\n'))#.strip()
            #print(record)
            taxonomy_id = record[0]
            Kingdom_name = record[1]
            Phylum_name = record[2]
            Family_name = record[5]
            Genus_name = record[6]
            latin_name = record[-1]
            
            if latin_name.startswith('uncultured'):
                Genus_name = re.split('\s+',latin_name)[1]
            else:
                Genus_name = re.split('\s+',latin_name)[0]
            out.write('\t'.join([taxonomy_id,Kingdom_name,Phylum_name,Family_name,Genus_name,latin_name])+'\n')


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
