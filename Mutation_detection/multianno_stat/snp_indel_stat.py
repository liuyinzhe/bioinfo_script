#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
import gzip
import os
import argparse
import sys
import re
from argparse import RawTextHelpFormatter

###Name:    statVariation.py
###Usage:   Aims to statistics SNP/InDel information from variation result and annotation files.


parser = argparse.ArgumentParser(
    description="vcf counts", formatter_class=RawTextHelpFormatter)
parser.add_argument('--snp', help="snp result . *._multianno.snp.txt ")
parser.add_argument('--indel', help="indel result . *._multianno.indel.txt")
parser.add_argument('--odir', help='out dir')
argv = vars(parser.parse_args())

snp = argv['snp']
indel = argv['indel']

if not snp and not indel:
    parser.print_help()
    sys.exit(1)


if argv['odir']:
    odir = argv['odir']
else:
    odir = os.getcwd()

if not os.path.exists(odir):
    assert not os.makedirs(odir)


def safe_open(file_name, mode):
    try:
        if not file_name.endswith('.gz'):
            return open(file_name, mode, encoding='utf-8')
        else:
            return gzip.open(file_name, mode)
    except IOError:
        print(file_name + ' does not exist!')


def isTs(ref, alt):
    geno = ref.upper()+alt.upper()
    if re.match("^[AG]+$", geno) or re.match("^[CT]+$", geno):
        return 1
    else:
        return 0


if snp:
    tstv = {}
    tstv["ts"] = 0
    tstv["tv"] = 0
    tstv_ratio = 0
    total_num = 0
    total_num_main = 0
    anno_type = {}
    anno_type_lst = ['Intergenic', 'Upstream', 'Downstream', 'Exonic', 'Splicing', 'Intronic', 'UTR3', 'UTR5', 'Upstream/Downstream',
                     'NcRNA_exonic', 'NcRNA_intronic', 'NcRNA_splicing', 'NcRNA_exonic/Splicing', 'UTR5/UTR3', 'Exonic/Splicing', 'NcRNA_UTR5', 'Other', 'Start loss', 'Stop gain', 'Stop loss', 'Synonymous', 'Non-synonymous', 'Unknown']

    for x in anno_type_lst:
        anno_type[x] = 0

    hetero = {'hete': 0, 'homo': 0}  # "hete","homo"

    with safe_open(snp, 'r') as txt:
        for line in txt:
            if line.startswith("Chr\t"):
                continue
            elif not line.startswith("#"):
                records = line.strip().split("\t")
                Chr = records[0]
                Start = records[1]
                End = records[2]
                ref = records[3]
                alt = records[4]
                Func = records[5]
                Gene = records[6]
                GeneDetail = records[7]
                ExonicFunc = records[8]
                total_num += 1
                ##ts/tv
                ref = records[3].split(",")[0]
                alt = records[4].split(",")[0]
                if isTs(ref, alt):
                    tstv["ts"] += 1
                else:
                    tstv["tv"] += 1
                '''Stop gain    Stop loss   Synonymous  Non-synonymous
                synonymous
                nonsynonymous
                '''
                if Func == 'exonic':
                    total_num_main += 1
                    if re.match('nonsynonymous', ExonicFunc):
                        anno_type['Non-synonymous'] += 1
                    elif re.match('synonymous', ExonicFunc):
                        anno_type['Synonymous'] += 1
                    elif re.match('stopgain', ExonicFunc):
                        anno_type['Stop gain'] += 1
                    elif re.match('stoploss', ExonicFunc):
                        anno_type['Stop loss'] += 1
                    elif re.match('startloss', ExonicFunc):
                        total_num_main -= 1
                        anno_type['Start loss'] += 1
                    elif re.match('unknown', ExonicFunc) or ExonicFunc == '.':
                        total_num_main -= 1
                        anno_type['Unknown'] += 1
                elif Func == 'intergenic':
                    #total_num_main += 1
                    anno_type['Intergenic'] += 1
                elif Func == 'upstream':
                    anno_type['Upstream'] += 1
                elif Func == 'downstream':
                    #total_num_main += 1
                    anno_type['Downstream'] += 1
                elif Func == 'splicing':
                    #total_num_main += 1
                    anno_type['Splicing'] += 1
                elif Func == 'intronic':
                    total_num_main += 1
                    anno_type['Intronic'] += 1
                elif Func == 'UTR3':
                    #total_num_main += 1
                    anno_type['UTR3'] += 1
                elif Func == 'UTR5':
                    total_num_main += 1
                    anno_type['UTR5'] += 1
                elif Func == 'upstream;downstream':
                    #total_num_main += 1
                    anno_type['Upstream/Downstream'] += 1
                elif Func == 'ncRNA_exonic':
                    anno_type['NcRNA_exonic'] += 1
                elif Func == 'ncRNA_intronic':
                    anno_type['NcRNA_intronic'] += 1
                elif Func == 'ncRNA_splicing':
                    anno_type['NcRNA_splicing'] += 1
                elif Func == 'ncRNA_exonic;splicing':
                    anno_type['NcRNA_exonic/Splicing'] += 1
                elif Func == 'UTR5;UTR3':
                    anno_type['UTR5/UTR3'] += 1
                elif Func == 'exonic;splicing':
                    anno_type['Exonic/Splicing'] += 1
                elif Func == 'ncRNA_UTR5':
                    anno_type['NcRNA_UTR5'] += 1
                else:
                    anno_type['Other'] += 1

            ##heterozygous
            #print(records[-1])
            alleles = re.split('[/|]', records[-1].split(":")[0])
            #print(alleles)
            if not alleles[0] == alleles[1]:
                hetero['hete'] += 1
            elif alleles[0] == alleles[1]:
                hetero['homo'] += 1

    ###ts/tv
    tstv_ratio = "%0.3f" % (tstv["ts"]/tstv["tv"])
    # ['Upstream', 'Stop gain','Stop loss', 'Synonymous', 'Non-synonymous', 'Intronic', 'Splicing', 'Downstream', 'Upstream/Downstream', 'Intergenic']
    other_num = total_num - total_num_main
    anno_type['other'] = other_num
    anno_type['total_num'] = total_num
    anno_type['tstv_ratio'] = tstv_ratio
    #snp_table_header = ['Upstream', 'Stop gain', 'Stop loss', 'Synonymous', 'Non-synonymous', 'Intronic', 'Splicing', 'Downstream',
    #                    'Upstream/Downstream', 'Intergenic', 'other', 'total_num', 'tstv_ratio']
    snp_table_header = ['UTR5', 'Stop gain', 'Stop loss', 'Synonymous', 'Non-synonymous', 'Intronic',
                        'other', 'total_num', 'tstv_ratio']
    snp_table_header_str = "\t".join(snp_table_header)
    #anno_type_lst = [  'UTR5', 'Exonic/Splicing', 'UTR3','UTR5/UTR3', 'NcRNA_UTR5','NcRNA_splicing','NcRNA_exonic/Splicing','NcRNA_exonic', 'NcRNA_intronic', 'Other']
    #anno_type['exonic'] = {'Start loss': 0，'Unknown': 0}
    #
    snp_table_lst = []
    for x in snp_table_header:
        snp_table_lst.append(str(anno_type[x]))
    snp_table_str = '\t'.join(snp_table_lst)

    small_snp_tab = "small_tab.snp.stat.txt"

    with open(small_snp_tab, mode='w', encoding='utf-8') as out:
        out.write(snp_table_header_str+"\n")
        out.write(snp_table_str + "\n")

    full_snp_table_header = ['Upstream', 'UTR5', 'Start loss', 'Stop gain', 'Stop loss', 'Synonymous', 'Non-synonymous', 'Unknown', 'Intronic', 'Exonic/Splicing',  'Splicing', 'UTR3',
                             'Downstream',  'Upstream/Downstream', 'Intergenic', 'NcRNA_exonic', 'NcRNA_intronic', 'NcRNA_splicing', 'NcRNA_exonic/Splicing', 'UTR5/UTR3', 'Exonic/Splicing', 'NcRNA_UTR5', 'other', 'total_num', 'tstv_ratio']
    #'Stop gain','Stop loss', 'Synonymous', 'Non-synonymous'
    full_snp_table_header_str = "\t".join(full_snp_table_header)

    full_snp_table_lst = []
    for x in full_snp_table_header:
        full_snp_table_lst.append(str(anno_type[x]))
    full_snp_table_str = '\t'.join(full_snp_table_lst)

    full_snp_tab = "full_tab.snp.stat.txt"
    with open(full_snp_tab, mode='w', encoding='utf-8') as out:
        out.write(full_snp_table_header_str + "\n")
        out.write(full_snp_table_str + "\n")


if indel:
    total_num = {}
    indel_length = {}
    anno_type = {}
    total_num = 0
    total_num_main = 0
    anno_type = {}
    anno_type_lst = ['Intergenic', 'Upstream', 'Downstream', 'Exonic', 'Splicing', 'Intronic', 'UTR3', 'UTR5', 'Upstream/Downstream',
                     'NcRNA_exonic', 'NcRNA_intronic', 'NcRNA_splicing', 'NcRNA_exonic/Splicing', 'UTR5/UTR3', 'Exonic/Splicing', 'NcRNA_UTR5', 'Other', 'Start loss', 'Stop gain', 'Stop loss', 'Non-frameshift insertion', 'Non-frameshift deletion', 'Frameshift insertion', 'Frameshift deletion', 'Unknown', 'Deletion', 'Insertion']

    for x in anno_type_lst:
        anno_type[x] = 0

    for line in safe_open(indel, 'r'):  #
        if line.startswith("Chr\t"):
            continue
        elif not line.startswith("#"):
            records = line.strip().split("\t")
            Chr = records[0]
            Start = records[1]
            End = records[2]
            ref = records[3]
            alt = records[4]
            Func = records[5]
            Gene = records[6]
            GeneDetail = records[7]
            ExonicFunc = records[8]
            total_num += 1

            #
            ##Deletion/Insertion
            #Frameshift deletion    Frameshift insertion    Non-frameshift deletion Non-frameshift insertion
            if ref == '-':
                anno_type['Deletion'] += 1
            else:
                anno_type['Insertion'] += 1

            '''Stop gain    Stop loss   Synonymous  Non-synonymous
            synonymous
            nonsynonymous
            '''

            if Func == 'exonic':
                total_num_main += 1
                if re.match('frameshift deletion', ExonicFunc):
                    anno_type['Frameshift deletion'] += 1
                if re.match('frameshift insertion', ExonicFunc):
                    anno_type['Frameshift insertion'] += 1
                if re.match('nonframeshift deletion', ExonicFunc):
                    anno_type['Non-frameshift deletion'] += 1
                elif re.match('nonframeshift insertion', ExonicFunc):
                    anno_type['Non-frameshift insertion'] += 1
                elif re.match('stopgain', ExonicFunc):
                    anno_type['Stop gain'] += 1
                elif re.match('stoploss', ExonicFunc):
                    anno_type['Stop loss'] += 1
                elif re.match('startloss', ExonicFunc):
                    total_num_main -= 1
                    anno_type['Start loss'] += 1
                elif re.match('unknown', ExonicFunc) or ExonicFunc == '.':
                    total_num_main -= 1
                    anno_type['Unknown'] += 1
            elif Func == 'intergenic':
                #total_num_main += 1
                anno_type['Intergenic'] += 1
            elif Func == 'upstream':
                anno_type['Upstream'] += 1
            elif Func == 'downstream':
                #total_num_main += 1
                anno_type['Downstream'] += 1
            elif Func == 'splicing':
                #total_num_main += 1
                anno_type['Splicing'] += 1
            elif Func == 'intronic':
                total_num_main += 1
                anno_type['Intronic'] += 1
            elif Func == 'UTR3':
                #total_num_main += 1
                anno_type['UTR3'] += 1
            elif Func == 'UTR5':
                total_num_main += 1
                anno_type['UTR5'] += 1
            elif Func == 'upstream;downstream':
                #total_num_main += 1
                anno_type['Upstream/Downstream'] += 1
            elif Func == 'ncRNA_exonic':
                anno_type['NcRNA_exonic'] += 1
            elif Func == 'ncRNA_intronic':
                anno_type['NcRNA_intronic'] += 1
            elif Func == 'ncRNA_splicing':
                anno_type['NcRNA_splicing'] += 1
            elif Func == 'ncRNA_exonic;splicing':
                anno_type['NcRNA_exonic/Splicing'] += 1
            elif Func == 'UTR5;UTR3':
                anno_type['UTR5/UTR3'] += 1
            elif Func == 'exonic;splicing':
                anno_type['Exonic/Splicing'] += 1
            elif Func == 'ncRNA_UTR5':
                anno_type['NcRNA_UTR5'] += 1
            else:
                anno_type['Other'] += 1

    other_num = total_num - total_num_main

    #anno_type_lst = ['Intergenic', 'Upstream', 'Downstream', 'Exonic', 'Splicing', 'Intronic', 'UTR3', 'UTR5', 'Upstream/Downstream',
    #                 'NcRNA_exonic', 'NcRNA_intronic', 'NcRNA_splicing', 'NcRNA_exonic/Splicing', 'UTR5/UTR3', 'Exonic/Splicing', 'NcRNA_UTR5', 'Other', 'Start loss', 'Stop gain', 'Stop loss', 'Synonymous', 'Non-synonymous', 'Unknown', 'Deletion', 'Insertion']

    anno_type['other'] = other_num
    anno_type['total_num'] = total_num
    indel_table_header = ['UTR5', 'Stop gain', 'Stop loss', 'Frameshift insertion', 'Frameshift deletion', 'Non-frameshift insertion', 'Non-frameshift deletion', 'Intronic',
                          'other', 'Deletion', 'Insertion']
    indel_table_header_str = "\t".join(indel_table_header)
    #anno_type_lst = [  'UTR5', 'Exonic/Splicing', 'UTR3','UTR5/UTR3', 'NcRNA_UTR5','NcRNA_splicing','NcRNA_exonic/Splicing','NcRNA_exonic', 'NcRNA_intronic', 'Other']
    #anno_type['exonic'] = {'Start loss': 0，'Unknown': 0}
    #
    indel_table_lst = []
    for x in indel_table_header:
        indel_table_lst.append(str(anno_type[x]))
    indel_table_str = '\t'.join(indel_table_lst)

    small_indel_tab = "small_tab.indel.stat.txt"

    with open(small_indel_tab, mode='w', encoding='utf-8') as out:
        out.write(indel_table_header_str+"\n")
        out.write(indel_table_str + "\n")

    full_indel_table_header = ['Upstream', 'UTR5', 'Start loss', 'Stop gain', 'Stop loss', 'Frameshift insertion', 'Frameshift deletion', 'Non-frameshift insertion', 'Non-frameshift deletion', 'Unknown', 'Intronic', 'Exonic/Splicing',  'Splicing', 'UTR3',
                               'Downstream',  'Upstream/Downstream', 'Intergenic', 'NcRNA_exonic', 'NcRNA_intronic', 'NcRNA_splicing', 'NcRNA_exonic/Splicing', 'UTR5/UTR3', 'Exonic/Splicing', 'NcRNA_UTR5', 'other', 'total_num', 'Deletion', 'Insertion']
    #'Stop gain','Stop loss', 'Synonymous', 'Non-synonymous'
    full_indel_table_header_str = "\t".join(full_indel_table_header)

    full_indel_table_lst = []
    for x in full_indel_table_header:
        full_indel_table_lst.append(str(anno_type[x]))
    full_indel_table_str = '\t'.join(full_indel_table_lst)

    full_indel_tab = "full_tab.indel.stat.txt"
    with open(full_indel_tab, mode='w', encoding='utf-8') as out:
        out.write(full_indel_table_header_str + "\n")
        out.write(full_indel_table_str + "\n")
