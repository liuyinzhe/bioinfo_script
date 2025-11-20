mitoz annotate \
  --outprefix mitoz \
  --species_name 'latin name' \
  --fastafiles  mitochondrion.fasta \
  --clade Chordata

# genbank 输出模板需要修改或者指定
#  --template_sbt <file>
#                        The sqn template to generate the resulting genbank file. Go to https://www.ncbi.nlm.nih.gov/genbank/tbl2asn2/#Template to generate your own template file if you
#                        like. ['~/envs/mitoz3.6/lib/python3.8/site-packages/mitoz/annotate/script/template.sbt']

# clade
# Chordata	脊索动物门
# Arthropoda	节肢动物门
# Echinodermata	棘皮动物门
# Annelida-segmented-worms	环节动物门 分节蠕虫
# Bryozoa	苔藓动物门
# Mollusca	软体动物门
# Nematoda	线形动物门
# Nemertea-ribbon-worms 纽形动物门 带状蠕虫
# Porifera-sponges	多孔动物门 海绵
