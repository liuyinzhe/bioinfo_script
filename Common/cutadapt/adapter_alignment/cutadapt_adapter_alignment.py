import re
from cutadapt.adapters import (
    FrontAdapter,
    BackAdapter,
    PrefixAdapter,
    SuffixAdapter,
    AnywhereAdapter,
    LinkedAdapter,
)
from dnaio import SequenceRecord
from cutadapt.modifiers import AdapterCutter, ModificationInfo

def get_adapter_alignment(adapter_seq,read_seq,max_mismatch,Adapter_type='AnywhereAdapter',cutter_action='lowercase',min_overlap=None,indels_bool=True):
    '''
    parameter:
    adapter_seq # adapter sequence
    read_seq # read sequence
    max_mismatch # 最大错配数
    min_overlap # 最小重叠数
    indels = True # 是否允许插入和删除
    Adapter_type = [PrefixAdapter,SuffixAdapter,FrontAdapter,BackAdapter,AnywhereAdapter]

    returns:
        position_lst [ list or None boolean False ]
        trimmed_read
    '''
    adapter_seq = adapter_seq.upper()

    
    read_obj = SequenceRecord("foo", read_seq)
    read_seq = read_obj.sequence
    adapter_len = len(adapter_seq)
    
    if max_mismatch > 0 :
        percent = max_mismatch/adapter_len
        #print(percent,max_mismatch,adapter_len)
        max_errors =percent + 1/(10*(len(str(percent).split('.')[1])+1))
        if max_mismatch>=adapter_len:
            max_errors = 0
            min_overlap = adapter_len
        elif not min_overlap:
            min_overlap = int(adapter_len/2)
    else:
        max_errors = 0
        min_overlap = adapter_len
    #print(max_errors,min_overlap)
    # PrefixAdapter # 非内部接头，自定义，只匹配最开头出现的
    # SuffixAdapter # 非内部接头，自定义，只匹配末端出现的
    # FrontAdapter  # 接头前测的一并注释为接头 # RemoveBeforeMatch
    # BackAdapter   # 接头后侧的一并注释为接头 # RemoveAfterMatch
    # AnywhereAdapter # 任何位置都可以搜索，先搜5’前面，后缩后面,分别使用 FrontAdapter,BackAdapter,cutter时会trim 处理接头以外的序列
    if Adapter_type == "PrefixAdapter":
        adapter = PrefixAdapter(
                                    sequence=adapter_seq, #RemoveAfterMatch
                                    max_errors=max_errors,
                                    min_overlap=min_overlap,
                                    read_wildcards=False, #N
                                    adapter_wildcards=False, #N
                                    indels=indels_bool
                                    )
    elif Adapter_type == "SuffixAdapter":
        adapter = SuffixAdapter(
                                    sequence=adapter_seq, #RemoveAfterMatch
                                    max_errors=max_errors,
                                    min_overlap=min_overlap,
                                    read_wildcards=False, #N
                                    adapter_wildcards=False, #N
                                    indels=indels_bool
                                    )
    elif Adapter_type == "FrontAdapter":
        adapter = FrontAdapter(
                                    sequence=adapter_seq, #RemoveAfterMatch
                                    max_errors=max_errors,
                                    min_overlap=min_overlap,
                                    read_wildcards=False, #N
                                    adapter_wildcards=False, #N
                                    indels=indels_bool
                                    )
    elif Adapter_type == "BackAdapter":
        adapter = BackAdapter(
                                    sequence=adapter_seq, #RemoveAfterMatch
                                    max_errors=max_errors,
                                    min_overlap=min_overlap,
                                    read_wildcards=False, #N
                                    adapter_wildcards=False, #N
                                    indels=indels_bool
                                    )
    elif Adapter_type == "AnywhereAdapter":
        adapter = AnywhereAdapter(
                                    sequence=adapter_seq, #RemoveAfterMatch
                                    max_errors=max_errors,
                                    min_overlap=min_overlap,
                                    read_wildcards=False, #N
                                    adapter_wildcards=False, #N
                                    indels=indels_bool
                                    )
    else:
        raise Exception("Illegal Adapter type:", Adapter_type)
    alignment_obj = adapter.match_to(read_seq)
    #RemoveBeforeMatch(astart=0, astop=4, rstart=0, rstop=4, score=4, errors=0)
    if alignment_obj:
        astart = alignment_obj.astart
        astop = alignment_obj.astop
        rstart = alignment_obj.rstart
        rstop = alignment_obj.rstop
        score = alignment_obj.score
        errors = alignment_obj.errors
        position_lst = [astart,astop,rstart,rstop,score,errors]

        # Trim 
        # class AdapterCutter(SingleEndModifier):
        #     """
        #     Repeatedly find one of multiple adapters in reads.

        #     Arguments:
        #         adapters: Adapters to be searched
        #         times: Repeat the search this number of times.
        #         action: What to do with a found adapter.
        #             - *None*: Do nothing, only update the ModificationInfo appropriately
        #             - "trim": Remove the adapter and down- or upstream sequence depending on adapter type
        #             - "mask": Replace the part of the sequence that would have been removed with "N" bases
        #             - "lowercase": Convert the part of the sequence that would have been removed to lowercase
        #             - "retain": Like "trim", but leave the adapter sequence itself in the read
        #         index: If True, attempt to create an index to speed up the search (if possible)
        #     """
        cutter = AdapterCutter([adapter], times=1,action=cutter_action)
        trimmed_read = cutter(read_obj, ModificationInfo(read_obj))
        return position_lst,trimmed_read
    else:
        return None,read_seq

adapter_seq='TCCGCTTAGAGGACT'.upper()
read_seq='GACACTACTAGTGCTCGCTTAGAGGACTAATTCTGCAGTCGAGACCTAGAAAAACATGGAGCAATCACAAGTAGCAATACAGCAGCTACCAATGCTGATTGTGCCTGGCTAGAAGCACAAGAGGAGGAGGAGGTGGGTTTTCCAGTCACAC'.upper()
print(adapter_seq)
print(read_seq)
max_mismatch=1
position_lst = get_adapter_alignment(adapter_seq,read_seq,max_mismatch)
print(position_lst)
astart,astop,rstart,rstop,score,errors = position_lst
x=read_seq[rstart:rstop]
print(read_seq[rstart:rstop])
print(re.split(x,read_seq,maxsplit=1))




def test_linked_adapter():
    front_adapter = PrefixAdapter("AAAA", min_overlap=4) ##可以详细设置，因为front_required=True, 所以使用的是PrefixAdapter，而不是FrontAdapter，全部位置匹配
    back_adapter = BackAdapter("TTTT", min_overlap=3)

    linked_adapter = LinkedAdapter(
        front_adapter,
        back_adapter,
        front_required=True,
        back_required=False,
        name="name",
    )
    assert linked_adapter.front_adapter.min_overlap == 4
    assert linked_adapter.back_adapter.min_overlap == 3

    read = SequenceRecord(name="seq", sequence="AAAACCCCCTTTT")
    #print(linked_adapter.match_to(read.sequence))
    '''
    <LinkedMatch(front_match=RemoveBeforeMatch(astart=0, astop=4, rstart=0, rstop=4, score=4, errors=0), back_match=RemoveAfterMatch(astart=0, astop=4, rstart=5, rstop=9, score=4, errors=0), adapter=LinkedAdapter(front_adapter=<PrefixAdapter(name='name', sequence='AAAA', max_error_rate=0.1, min_overlap=4, read_wildcards=False, adapter_wildcards=False, indels=True)>, back_adapter=<BackAdapter(name='2', sequence='TTTT', max_error_rate=0.1, min_overlap=3, read_wildcards=False, adapter_wildcards=False, indels=True)>))>
    '''
    trimmed = linked_adapter.match_to(read.sequence).trimmed(read) # trimmed 使用 RemoveBeforeMatch RemoveAfterMatch 进行trim
    #print(trimmed) # CCCCC
    assert trimmed.name == "seq"
    assert trimmed.sequence == "CCCCC"
