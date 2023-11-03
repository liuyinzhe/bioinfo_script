export BUGBASE_PATH=/data/software/BugBase
export PATH=$PATH:/data/software/BugBase/bin

#NOTE#输入的 biom 输入的需要是 使用 GreenGenes database注释taxonomy

rm -rf output/
/data/envs/R332/bin/Rscript ${BUGBASE_PATH}/bin/run.bugbase.r \
   -t 2 \
   -i table.from_txt_json.biom \
   -m map.txt \
   -c BODY_SITE \
   -o ${PWD}/output

#   --threshold=0.5 \
#   -i otu_table.txt \
#   -g "S12,S13,S14,S27,S28,S29,S35,S38,S39,S40,S41,S42,S43,S58,S62,S63,S64,S65,S66,S67,S73,S75,S76" \

# otu_table.txt 作为输入 需要 去掉第一行# Constructed from biom file  和最后一列 taxonomy


#参数 --taxalevel
#        -t TAXALEVEL, --taxalevel=TAXALEVEL
#                taxa level to plot otu contributions by, default is 
#              2 (phylum) [default NULL]

#界（Kingdom）、门（Phylum）、纲（Class）、目（Order）、科（Family）、属（Genus）、种（Species）
#     1              2           3             4            5             6             7     
