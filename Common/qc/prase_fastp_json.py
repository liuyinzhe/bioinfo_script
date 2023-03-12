import json
import re
import os
from pathlib import Path

def parse_fastp_json(sample,fastp_json):
    '''
    ['summary', 'filtering_result', 'duplication', 'insert_size', 'adapter_cutting', 'read1_before_filtering', 'read2_before_filtering', 'read1_after_filtering', 'read2_after_filtering', 'command']
    summary
    {'fastp_version': '0.23.2', 
    'sequencing': 'paired end (150 cycles + 150 cycles)', 
    'before_filtering': {'total_reads': 32928942, 
                            'total_bases': 4939341300, 
                            'q20_bases': 4799149191, 
                            'q30_bases': 4562166407, 
                            'q20_rate': 0.971617, 
                            'q30_rate': 0.923639, 
                            'read1_mean_length': 150, 
                            'read2_mean_length': 150, 
                            'gc_content': 0.497329}, 
    'after_filtering': {'total_reads': 32584076, 
                        'total_bases': 4845281409, 
                        'q20_bases': 4722496735, 
                        'q30_bases': 4493950619, 
                        'q20_rate': 0.974659, 
                        'q30_rate': 0.92749, 
                        'read1_mean_length': 148, 
                        'read2_mean_length': 148, 
                        'gc_content': 0.497534}
    }

    filtering_result
    {'passed_filter_reads': 32584076, 
    'low_quality_reads': 329902, 
    'too_many_N_reads': 13264, 
    'too_short_reads': 1700, 
    'too_long_reads': 0
    }

    duplication
    {'rate': 0.357218}

    insert_size
    {
		"peak": 202,
		"unknown": 1048458,
		"histogram": [101,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,13,1,11,8,8,8,13,11,12,15,29,16,25,30,23,20,29,20,25,23,31,31,21,28,34,41,29,39,50,49,67,49,67,57,82,69,70,88,92,115,96,95,115,125,130,138,137,189,192,206,197,218,273,256,293,285,293,344,318,389,377,422,463,496,511,577,564,607,626,654,743,764,869,851,857,909,975,993,1026,1164,1170,1237,1212,1461,1352,1559,1599,1697,1587,1673,1794,1844,1908,2107,2135,2292,2326,2309,2480,2455,2576,2648,2786,3084,3215,3250,3329,3367,3370,3517,3497,3641,3966,4070,4220,4203,4480,4622,4671,4683,4723,4804,4992,5159,5233,5284,5577,5622,5761,5725,5647,5937,5740,6070,6206,6549,6623,6762,7072,6720,6953,6977,7013,6952,7091,7002,7512,7655,7706,7853,7604,7612,7817,7906,7974,8150,8240,8106,8300,8463,8033,8203,8147,8143,8104,8483,8446,8525,8754,8743,8802,8470,8414,8436,8566,8477,8525,8687,8461,8532,8239,8411,8479,8356,8115,8300,8197,8492,8114,8286,8549,8436,8376,8109,8197,8087,8126,8173,8045,8067,8223,8056,7883,7869,7775,7904,7554,7489,7634,7845,7797,7771,7493,7506,7088,7383,7196,7375,7136,7073,7291,7300,7067,7228,7381,6935,6962,6899,7010,7160,6849,6853,6795,6844,6660,6579,6775,6492,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	},

    adapter_cutting
        {
		"adapter_trimmed_reads": 1923784,
		"adapter_trimmed_bases": 40711935,
		"read1_adapter_sequence": "unspecified",
		"read2_adapter_sequence": "unspecified",
		"read1_adapter_counts": {"A":36301, "AG":35837, "AGA":34164, "AGAT":32513, "AGATC":31956, "AGATCG":30662, "AGATCGG":28542, "AGATCGGA":27936, "AGATCGGAA":27074, "AGATCGGAAG":26143, "AGATCGGAAGA":25909, "AGATCGGAAGAG":25055, "AGATCGGAAGAGC":24521, "AGATCGGAAGAGCA":24023, "AGATCGGAAGAGCAC":23007, "AGATCGGAAGAGCACA":21541, "AGATCGGAAGAGCACAC":20370, "AGATCGGAAGAGCACACG":19044, "AGATCGGAAGAGCACACGT":18912, "AGATCGGAAGAGCACACGTC":18497, "AGATCGGAAGAGCACACGTCT":17724, "AGATCGGAAGAGCACACGTCTG":17362, "AGATCGGAAGAGCACACGTCTGA":17118, "AGATCGGAAGAGCACACGTCTGAA":15784, "AGATCGGAAGAGCACACGTCTGAAC":14979, "AGATCGGAAGAGCACACGTCTGAACT":14364, "AGATCGGAAGAGCACACGTCTGAACTC":13462, "AGATCGGAAGAGCACACGTCTGAACTCC":13107, "AGATCGGAAGAGCACACGTCTGAACTCCA":12434, "AGATCGGAAGAGCACACGTCTGAACTCCAG":11820, "AGATCGGAAGAGCACACGTCTGAACTCCAGT":11741, "AGATCGGAAGAGCACACGTCTGAACTCCAGTC":11448, "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA":11189, "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC":10662, "AGATCGGAAGAGCACACGTCTGAACTCCAGTCACG":10242, "others":226277},
		"read2_adapter_counts": {"A":36264, "AG":35960, "AGA":34208, "AGAT":32518, "AGATC":32114, "AGATCG":30862, "AGATCGG":28670, "AGATCGGA":28026, "AGATCGGAA":26537, "AGATCGGAAG":25654, "AGATCGGAAGA":25398, "AGATCGGAAGAG":24397, "AGATCGGAAGAGC":24077, "AGATCGGAAGAGCG":23521, "AGATCGGAAGAGCGT":22445, "AGATCGGAAGAGCGTC":21040, "AGATCGGAAGAGCGTCG":19902, "AGATCGGAAGAGCGTCGT":18321, "AGATCGGAAGAGCGTCGTG":18154, "AGATCGGAAGAGCGTCGTGT":17283, "AGATCGGAAGAGCGTCGTGTA":16278, "AGATCGGAAGAGCGTCGTGTAG":16104, "AGATCGGAAGAGCGTCGTGTAGG":15804, "AGATCGGAAGAGCGTCGTGTAGGG":14544, "AGATCGGAAGAGCGTCGTGTAGGGA":13728, "AGATCGGAAGAGCGTCGTGTAGGGAA":12427, "AGATCGGAAGAGCGTCGTGTAGGGAAA":11813, "AGATCGGAAGAGCGTCGTGTAGGGAAAG":11481, "AGATCGGAAGAGCGTCGTGTAGGGAAAGA":10990, "AGATCGGAAGAGCGTCGTGTAGGGAAAGAG":10310, "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGT":11052, "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTG":9893, "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT":11226, "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTGAAC":22786, "others":248105}
	},
    '''
    summary_target_lst = ['total_reads', 'total_bases', 'q20_bases', 'q30_bases', 'q20_rate', 'q30_rate',  'gc_content']
    json_str = ""
    with open(fastp_json,mode='rt',encoding='utf-8') as fh:
        json_str = fh.read()
    fastp_dict = json.loads(json_str)
    #print(fastp_dict.keys())
    #print("#"*26)
    #print(fastp_dict['summary']['after_filtering'])
    
    summary_header = [sample,'raw reads','raw bases','clean reads','clean bases','valid bases',
                    'Q30','GC']
    
    summary_tab_lst = [sample,str(fastp_dict['summary']['before_filtering']['total_reads']), 
                     str(fastp_dict['summary']['before_filtering']['total_bases']), 
                     str(fastp_dict['summary']['after_filtering']['total_reads']),
                     str(fastp_dict['summary']['after_filtering']['total_bases']),
                     "{:.2f}%".format(int(fastp_dict['summary']['after_filtering']['total_bases'])/int(fastp_dict['summary']['before_filtering']['total_bases'])*100),
                     "{:.2f}%".format(float(fastp_dict['summary']['after_filtering']['q30_rate'])*100),
                     "{:.2f}%".format(float(fastp_dict['summary']['after_filtering']['gc_content'])*100)
                     ]


    before_filtering_lst = []
    after_filtering_lst = []
    for  key in summary_target_lst:
        #print(fastp_dict['summary']['before_filtering'][key])
        if key in ['q20_rate', 'q30_rate',  'gc_content']:
            before_filtering_lst.append(str(fastp_dict['summary']['before_filtering'][key]*100))
            after_filtering_lst.append(str(fastp_dict['summary']['after_filtering'][key]*100))
        else:
            before_filtering_lst.append(str(fastp_dict['summary']['before_filtering'][key]))
            after_filtering_lst.append(str(fastp_dict['summary']['after_filtering'][key]))

    # with open(sample+'.summary.tsv',mode='wt',encoding='utf-8') as out:
    #     out.write('\t'.join(summary_header)+'\n')
    #     out.write('\t'.join(summary_tab_lst)+'\n')
        
    # with open(sample+'.fastp_before.tsv',mode='wt',encoding='utf-8') as out1,open(sample+'.fastp_after.tsv',mode='wt',encoding='utf-8') as out2:
    #     #  ['total_reads', 'total_bases', 'q20_bases', 'q30_bases', 'q20_rate', 'q30_rate',  'gc_content']
    #     result_lst = []
    #     out1.write('\t'.join(summary_target_lst)+"\n")
    #     for  key in summary_target_lst:
    #         #print(fastp_dict['summary']['before_filtering'][key])
    #         if key in ['q20_rate', 'q30_rate',  'gc_content']:
    #             result_lst.append(str(fastp_dict['summary']['before_filtering'][key]*100))
    #         else:
    #             result_lst.append(str(fastp_dict['summary']['before_filtering'][key]))
    #     out1.write('\t'.join(result_lst)+"\n")

    #     result_lst = []
    #     out2.write('\t'.join(summary_target_lst)+"\n")
    #     for  key in summary_target_lst:
    #         if key in ['q20_rate', 'q30_rate',  'gc_content']:
    #             result_lst.append(str(fastp_dict['summary']['after_filtering'][key]*100))
    #         else:
    #             result_lst.append(str(fastp_dict['summary']['after_filtering'][key]))
    #     out2.write('\t'.join(result_lst)+"\n")

    return summary_header,summary_tab_lst,summary_target_lst,before_filtering_lst,after_filtering_lst

def GetAllFileNames(pwd,wildcard='*'):
    '''
    获取目录下所有文件名，返回列表
    param: str  "pwd"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    #字符串路径 工厂化为 pathlib 对象，可使用pathlib 对象的方法(函数)/属性(私有变量)
    target_path = Path(pwd)
    for child in target_path.glob(wildcard):
        if child.is_dir():
            pass
        elif child.is_file():
            #child完整路径,child.relative_to(pwd) 相对于pwd的相对路径，其实就是文件名;可以通过child.name获得
            files_lst.append(child.relative_to(pwd))
            #print(child.relative_to(pwd))
    return files_lst

def main():

    ## 跳转脚本所在目录
    pwd = os.path.split(os.path.realpath(__file__))[0]
    #pwd = os.getcwd()
    pwd = Path(pwd)
    os.chdir(pwd)
    name_list = GetAllFileNames(pwd,wildcard='*.qc.fastp.json')
    sample_name_lst = [re.split(r"\.",str(x))[0] for x in name_list]
    #print(sample_name_lst)
    for sample in sample_name_lst:
        fastp_json_path = pwd.joinpath(sample+".qc.fastp.json")
        summary_header,summary_tab_lst,summary_target_lst,before_filtering_lst,after_filtering_lst = parse_fastp_json(sample,fastp_json_path)
        
        with open(sample+'.summary.tsv',mode='wt',encoding='utf-8') as out:
            out.write('\t'.join(summary_header)+'\n')
            out.write('\t'.join(summary_tab_lst)+'\n')
        
        with open(sample+'.fastp_before.tsv',mode='wt',encoding='utf-8') as out1,open(sample+'.fastp_after.tsv',mode='wt',encoding='utf-8') as out2:
            #  ['total_reads', 'total_bases', 'q20_bases', 'q30_bases', 'q20_rate', 'q30_rate',  'gc_content']
            out1.write('\t'.join(summary_target_lst)+"\n")
            out1.write('\t'.join(before_filtering_lst)+"\n")

            out2.write('\t'.join(summary_target_lst)+"\n")
            out2.write('\t'.join(after_filtering_lst)+"\n")


if __name__ == '__main__':
    main()
