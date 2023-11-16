import gzip
import re

chrom_ord_dic = {
'1':'1',
'2':'2',
'3':'3',
'4':'4',
'5':'5',
'6':'6',
'7':'7',
'8':'8',
'9':'9',
'10':'10',
'11':'11',
'12':'12',
'13':'13',
'14':'14',
'15':'15',
'16':'16',
'17':'17',
'18':'18',
'19':'19',
'20':'20',
'21':'r21',
'22':'22',
'23':'X',
'24':'Y',
'12920':'M'
}
sub_name_dic = {}
with gzip.open('GCF_000001405.40.gz',mode='rt') as fh:
    for line in fh:
        if line.startswith('#'):
            print(line,end='')
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
            print(line,end='')
        else:
            print(line,end='')
