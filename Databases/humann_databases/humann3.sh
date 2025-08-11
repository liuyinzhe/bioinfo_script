# 安装环境
mamba create -y -n humann3 humann python==3.12
conda activate /data/home/liuyinzhe/software/miniconda3/envs/humann3

# 下载数据库
humann_databases --download chocophlan full /data/home/liuyinzhe/database/humann_databases --update-config yes 
humann_databases --download uniref uniref90_diamond /data/home/liuyinzhe/database/humann_databases --update-config yes
humann_databases --download utility_mapping full /data/home/liuyinzhe/database/humann_databases --update-config yes

## 更新格式：humann_config --update <section> <name> <value>
humann_config --update database_folders nucleotide /data/home/liuyinzhe/database/humann_databases/chocophlan
humann_config --update database_folders protein /data/home/liuyinzhe/database/humann_databases/uniref
humann_config --update database_folders utility_mapping /data/home/liuyinzhe/database/humann_databases/utility_mapping

## 更新后查看设置 验证
humann_config
