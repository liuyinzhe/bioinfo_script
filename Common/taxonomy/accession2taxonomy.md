## NCBI accession2taxonomy

#### 1.数据库下载
```bash
# taxdmp
wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip 
# accession2taxid
wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz 
```


#### 2 格式整理

```bash
grep "scientific name" names.dmp | awk -F"|" '{print $1,$2}' |sed 's/\t \t/\t/' > tax_id2name.txt  

nohup cut -f 1  tax_id2name.txt  | taxonkit lineage --data-dir ./ | taxonkit reformat --data-dir ./ -a  -f "{k};{p};{c};{o};{f};{g};{s}" > taxon_lineage_tmp 2>err &  

cut -f 1,3 taxon_lineage_tmp |awk -F ";" 'BEGIN{OFS="\t";}{print $1,$2,$3,$4,$5,$6,$7;}' >taxon_lineage.tsv    
```

>格式处理
```python
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
```
- [x] eXps
