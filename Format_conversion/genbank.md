#### Genbank

##### 在线工具 GenBank2Sequin
https://chlorobox.mpimp-golm.mpg.de/GenBank2Sequin.html

##### 本地脚本
https://ftp.ncbi.nlm.nih.gov//toolbox/ncbi_tools/converters/scripts/gbf2tbl.pl

#####  bp_genbank2gff3 (bio-perl)
perl-bioperl perl-yaml
https://github.com/bioperl/bioperl-live/blob/master/bin/bp_genbank2gff3

#### genbank2gff
https://github.com/ihh/gfftools/blob/master/genbank2gff.pl

##### biopython
```bash
pip install biopython bcbio-gff
```
```python
from BCBio import GFF
from Bio import SeqIO

in_file = "your_file.gb"
out_file = "your_file.gff"
in_handle = open(in_file)
out_handle = open(out_file, "w")

GFF.write(SeqIO.parse(in_handle, "genbank"), out_handle)

in_handle.close()
out_handle.close()
```

