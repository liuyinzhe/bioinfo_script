# funannotate Setup — Standalone Scripts

将 `funannotate setup` 命令拆分为**下载**（shell）和**处理**（Python）两个独立阶段，
可在无 funannotate Python 包的 Linux 环境中独立运行。

## 拆解逻辑

原 `funannotate setup` 命令做的事情：

```
                    ┌──────────────────────┐
                    │  funannotate setup   │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
   ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐
   │  设置目录     │   │  下载阶段     │   │  处理阶段         │
   │  加载URL列表  │   │  (网络I/O)   │   │  (CPU/磁盘I/O)    │
   └──────────────┘   └──────────────┘   └──────────────────┘
                              │                    │
                     download_all.sh        process_all.py
```

### download_all.sh (下载阶段)
- 纯 bash 脚本，仅需 `wget` 或 `curl`
- 从各公共数据库下载原始文件（FASTA / HMM / XML / OBO 等）
- 不做任何格式转换或索引构建

### process_all.py (处理阶段)
- 纯 Python 3 脚本，零 funannotate 依赖
- 需要外部工具: `diamond`, `hmmpress` (HMMER), `gunzip`, `tar`
- 执行: 解压 → 格式重排 → 构建 diamond/HMMER 索引 → 提取元数据 → 生成 `funannotate-db-info.txt`

## 快速开始

```bash
# 1. 下载所有数据库
bash download_all.sh -d /data/funannotate_db

# 2. 处理所有数据库
python process_all.py -d /data/funannotate_db

# 3. 设置环境变量
export FUNANNOTATE_DB=/data/funannotate_db
```

## 支持的数据库 (11 种)

| 数据库           | 下载内容                                          | 处理操作                          | 外部工具  |
|-----------------|---------------------------------------------------|----------------------------------|----------|
| **merops**      | `meropsscan.lib` (peptidase lib)                  | 重排FASTA头 → diamond makedb      | diamond  |
| **uniprot**     | `uniprot_sprot.fasta.gz` + release date           | gunzip → diamond makedb           | diamond  |
| **dbCAN**       | HMM db + family info + changelog                  | 重排NAME行 → hmmpress             | hmmpress |
| **pfam**        | `Pfam-A.hmm.gz` + clans + version                 | gunzip ×3 → hmmpress             | hmmpress |
| **repeats**     | repeat proteins `.tar.gz`                         | untar → 重排header → diamond      | diamond  |
| **go**          | `go.obo`                                          | 解析版本/术语计数 (仅元数据)       | (无)     |
| **mibig**       | `mibig_prot_seqs_*.fasta`                         | diamond makedb                    | diamond  |
| **interpro**    | `interpro.xml.gz` + entry list                    | gunzip → 解析XML元数据            | (无)     |
| **busco_outgroups** | pre-computed outgroups `.tar.gz`              | untar                             | (无)     |
| **gene2product**| `ncbi_cleaned_gene_products.txt`                  | 解析版本/记录数 (仅元数据)         | (无)     |
| **busco**       | 每个谱系一个 `.tar.gz` (28 个可选)                  | untar → 重命名目录                | (无)     |

## 选择性安装

```bash
# 仅下载特定数据库
bash download_all.sh -d /data/funannotate_db -i merops,uniprot,pfam

# 仅处理特定数据库
python process_all.py -d /data/funannotate_db -i merops,uniprot,pfam

# 指定 BUSCO 谱系
bash download_all.sh -d /data/funannotate_db -i busco -b "dikarya,fungi,sordariomycetes"
python process_all.py -d /data/funannotate_db -i busco -b "dikarya,fungi,sordariomycetes"

# 强制重新处理
python process_all.py -d /data/funannotate_db --force
```

## 外部工具依赖

在处理阶段需要以下工具在 `$PATH` 中：

| 工具       | 用途                           | 安装方式                              |
|-----------|-------------------------------|--------------------------------------|
| diamond   | 构建蛋白质序列比对数据库         | `conda install -c bioconda diamond`  |
| hmmpress  | 构建 HMMER profile 数据库      | `conda install -c bioconda hmmer`    |
| gunzip    | 解压 .gz 文件                  | 系统自带 (coreutils)                  |
| tar       | 解压 .tar.gz 文件              | 系统自带 (coreutils)                  |

## 输出结构

处理后 `$FUNANNOTATE_DB` 目录结构：

```
/path/to/funannotate_db/
├── funannotate-db-info.txt        # 数据库清单 (tab分隔)
├── meropsscan.lib                 # MEROPS 原始文件
├── merops.formatted.fa            # MEROPS 格式化后
├── merops.dmnd                    # MEROPS diamond索引
├── uniprot_sprot.fasta            # UniProt 解压后
├── uniprot.dmnd                   # UniProt diamond索引
├── uniprot.release-date.txt       # UniProt 发布日期
├── dbCAN.hmm + .h3{m,f,i,p}      # dbCAN HMMER 索引
├── dbCAN-fam-HMMs.txt             # dbCAN 家族信息
├── Pfam-A.hmm + .h3{m,f,i,p}     # Pfam HMMER 索引
├── Pfam-A.clans.tsv               # Pfam 家族分类
├── Pfam.version                   # Pfam 版本信息
├── funannotate.repeats.reformat.fa # Repeats 格式化后
├── repeats.dmnd                   # Repeats diamond索引
├── go.obo                         # GO 本体
├── mibig.fa                       # MiBIG 原始
├── mibig.dmnd                     # MiBIG diamond索引
├── interpro.xml                   # InterPro 解压后
├── interpro.tsv                   # InterPro 条目列表
├── ncbi_cleaned_gene_products.txt # 精选基因产物
├── outgroups/                     # BUSCO outgroups
├── trained_species/               # Augustus 预训练物种
├── fungi/                         # BUSCO 真菌谱系
├── dikarya/                       # BUSCO 双核亚界谱系
├── ...                            # 其他 BUSCO 谱系
```

## 工作流示意

```
┌─────────────────────────────────────────────────────┐
│                    Linux 服务器                       │
│                                                     │
│  1. download_all.sh                                 │
│     ├─ wget/curl → meropsscan.lib                   │
│     ├─ wget/curl → uniprot_sprot.fasta.gz           │
│     ├─ wget/curl → dbCAN-HMMdb-V12.txt              │
│     ├─ wget/curl → Pfam-A.hmm.gz                    │
│     ├─ ... (其余数据库)                               │
│     └─ wget/curl → fungi.tar.gz, dikarya.tar.gz...  │
│                                                     │
│  2. process_all.py                                  │
│     ├─ diamond makedb → merops.dmnd                  │
│     ├─ gunzip + diamond → uniprot.dmnd               │
│     ├─ hmmpress → dbCAN.hmm.h3*                      │
│     ├─ hmmpress → Pfam-A.hmm.h3*                     │
│     ├─ tar + diamond → repeats.dmnd                  │
│     ├─ (metadata extraction for go, mibig, etc.)    │
│     └─ → funannotate-db-info.txt                    │
│                                                     │
│  3. export FUNANNOTATE_DB=/path/to/funannotate_db   │
│     funannotate annotate -i ...                      │
└─────────────────────────────────────────────────────┘
```

## 与原 funannotate setup 的差异

| 方面             | 原 funannotate setup               | 本脚本                          |
|-----------------|------------------------------------|--------------------------------|
| 依赖            | funannotate Python 包 + 所有依赖    | 仅需 wget/curl + diamond + hmmer |
| URL 来源        | 从 GitHub 动态获取 downloads.json  | 直接硬编码在脚本中               |
| 更新检测        | 对比远程 MD5                       | 默认跳过已有文件（可 --force）    |
| 日志            | funannotate 日志系统               | 直接输出到终端                   |
| 进度条          | 有                                | 无                             |
| 错误处理        | 部分异常捕获                       | 每个数据库独立 try/catch         |
| Augustus species| 自动运行                          | 仅在 `$AUGUSTUS_CONFIG_PATH` 存在时运行 |
