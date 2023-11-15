
import gzip
import re

chrom_ord_dic = {
'1':'chr1',
'2':'chr2',
'3':'chr3',
'4':'chr4',
'5':'chr5',
'6':'chr6',
'7':'chr7',
'8':'chr8',
'9':'chr9',
'10':'chr10',
'11':'chr11',
'12':'chr12',
'13':'chr13',
'14':'chr14',
'15':'chr15',
'16':'chr16',
'17':'chr17',
'18':'chr18',
'19':'chr19',
'20':'chr20',
'21':'chr21',
'22':'chr22',
'23':'chrX',
'24':'chrY',
'12920':'chrM'
}
sub_name_dic = {}
with gzip.open('GCF_000001405.25.gz',mode='rt') as fh,gzip.open('GCF_000001405.25.new.gz',mode='wt') as out:
    for line in fh:
        if line.startswith('#'):
            out.write(line)
        elif line.startswith('NC_0'):
            chr_nc_id = re.split('\t',line)[0]
            if chr_nc_id in sub_name_dic:
                chr_name = sub_name_dic[chr_nc_id]
                line=re.sub(chr_nc_id,chr_name,line)
            else:
                match_obj = re.search('(NC_0{1,}(\d{1,})\.\d{1,2})',chr_nc_id)
                chr_nc_id = match_obj.group(0)
                chr_ord = match_obj.group(2)
                # print(line,)
                # print(chr_nc_id,chr_ord)
                chr_name = chrom_ord_dic[chr_ord]
                line=re.sub(chr_nc_id,chr_name,line)
                sub_name_dic[chr_nc_id] = chr_name
            out.write(line)
        else:
            out.write(line)
