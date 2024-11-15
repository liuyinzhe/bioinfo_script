def fasta2phy(fasta_dic):
    '''
    fasta_dic 中seq 长度必须一致
    '''
    seq_id_lst = list(fasta_dic.keys())
    record_count = len(seq_id_lst)
    seq_length = len(fasta_dic[seq_id_lst[0]])
    print('seq_length',seq_length)
    max_length = max([len(seq_id) for seq_id in seq_id_lst])
    print('max_length',max_length)

    '''
    序列拆分为10个碱基长度一个列表元素
    '''
    new_fasta_dic = {}
    for seq_id ,seq in fasta_dic.items():
        new_fasta_dic[seq_id] = [seq[i:i+10] for i in range(0, len(seq), 10)]
    #print(new_fasta_dic)
    '''
    5个元素一组,取序列，第一次前面是序列名，后面都是空字符，空格连接
    '''
    # 取整
    all_base_len = len(new_fasta_dic[seq_id_lst[0]])
    out_phy_seq = []
    seq_id_dic = {}
    last_idx = 0
    for  idx in range(0,all_base_len,5):
        last_idx = idx + 5
        #print(last_idx)
        for seq_id in seq_id_lst:
            sed_id_str = ""
            if seq_id not in seq_id_dic:
                seq_id_dic[seq_id] = 1
                sed_id_str = seq_id
            # 取序列的前5个元素
            seq_list = new_fasta_dic[seq_id][idx:idx+5]
            sed_id_out_str = sed_id_str.ljust(max_length)
            out_str = sed_id_out_str+" "+" ".join(seq_list)+'\n'
            #print(out_str)
            out_phy_seq.append(out_str)
        out_phy_seq.append("\n")
    # 取余,格局last index 继续取
    if seq_length>50 and seq_length%50 !=0:
        for seq_id in seq_id_lst:
            seq_list = new_fasta_dic[seq_id][last_idx:last_idx+5]#
            sed_id_out_str = "".ljust(max_length)
            out_str = sed_id_out_str+" "+" ".join(seq_list)+'\n'
            #print(out_str)
            out_phy_seq.append(out_str)

    with open("out.phy",mode='wt',encoding='utf-8') as out:
        out.write(" {record_count} {seq_length}\n".format(record_count=record_count,seq_length=seq_length))
        for out_phy in out_phy_seq:
            out.write(out_phy)
        
    return None
