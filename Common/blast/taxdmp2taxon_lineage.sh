
#grep "scientific name" names.dmp | awk -F"|" '{print $1,$2}'  >tax_id2name.txt
#grep "scientific name" names.dmp | awk -F"|" '{print $1,$2}' |sed 's/\t \t/\t/' > tax_id2name.txt

nohup cut -f 1  tax_id2name.txt  | taxonkit lineage --data-dir ./ | taxonkit reformat --data-dir ./ -a  -f "{k};{p};{c};{o};{f};{g};{s}" > taxon_lineage_tmp 2>err &
cut -f 1,3 taxon_lineage_tmp |awk -F ";" 'BEGIN{OFS="\t";}{print $1,$2,$3,$4,$5,$6,$7;}' >taxon_lineage.tsv
