import sys
import numpy as np
import json
import gzip

def calc_reads(numlist, threshold):
    base_count = 0
    reads_count = 0
    for line in numlist:
        if line > threshold:
            reads_count = reads_count + 1
            base_count += line 
    return base_count,reads_count


def calc_n(numlist, num):
    s = sum(numlist)
    sub = 0
    limit = s * 0.01 * num
    for l in sorted(numlist, reverse=True):
        sub = sub + l
        if sub >= limit:
            return l

#pass_qscore_list=[]
pass_len_list = []
#all_len_list = []
input_file=sys.argv[1]
num=0
with gzip.open(input_file, "rb") as gzfh:
    for line in gzfh:
        num += 1
        if num % 4 == 2:
            new_line = str(line,encoding='utf')
            read_len = len(new_line.strip())
            #print(read_len,new_line)
            pass_len_list.append(read_len)
        #print(pass_flag)
        #print(records[9])
        #pass_flag = False
        #print('True',"#"+records[9]+"#")
        #if records[9] == 'True' or records[9] == 'TRUE':
        #    pass_flag = True
        #elif records[9] == 'False' or records[9] == 'FALSE':
        #    pass_flag = False
        #print(pass_flag)
        #if pass_flag:
        #    #print(pass_len_list,read_len)
        #    #print(read_len)
        #    pass_len_list.append(read_len)
        #    #mean_qscore = float(records[14])
        #    #pass_qscore_list.append(mean_qscore)
            
#print(pass_len_list)


pass_base_num = sum(pass_len_list)
pass_read_num = len(pass_len_list)

total_base_num = pass_base_num
total_read_num = pass_read_num

pass_max_len = max(pass_len_list)
pass_mean_len = round(float(pass_base_num) / pass_read_num, 2)
pass_medium_len = int(np.median(pass_len_list))

#pass_mean_qscore = round(float(sum(pass_qscore_list) / pass_read_num), 2)
pass_n50_len = calc_n(pass_len_list, 50)


n_list = [10,20,30,40,50,60,70,80,90]
all_nx0 = {}
for num in n_list:
    name = "n"+str(num)
    #all_nx0[name] = calc_n(all_len_list, num)
    all_nx0[name] = calc_n(pass_len_list, num)
    
pass_nx0 = {}
n_list = [10,20,30,40,50,60,70,80,90]
for num in n_list:
    name = "n"+str(num)
    pass_nx0[name] = calc_n(pass_len_list, num)
    #print(pass_nx0[name])

pass_ultralong = {}
str_list=[50,80,100,200,300,400,500]
for x in str_list:
    threshold = x *1000
    key_str = ">"+str(x)+"Kb"
    base_count, reads_count = calc_reads(pass_len_list, threshold)
    pass_ultralong[key_str]={"base_num": base_count,"read_num": reads_count}
    #print({"base_num": base_count,"read_num": reads_count})

    
pass_gc_rate = 0
# write_json
fo = open("qc_stat.json", 'w')
fo.write(json.dumps({
    'total_base_num': total_base_num,
    'total_read_num': total_read_num,
    'pass_base_num': pass_base_num,
    'pass_read_num': pass_read_num,
    'pass_max_len': pass_max_len,
    'pass_mean_len': pass_mean_len,
    'pass_medium_len': pass_medium_len,
    'pass_mean_qscore': '0',
    'pass_n50_len': pass_n50_len,
    'pass_gc_rate': pass_gc_rate,
    'all_nx0': all_nx0,
    'pass_nx0': pass_nx0,
    'pass_ultralong': pass_ultralong
}, indent=4))
fo.close()
