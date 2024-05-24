from typing import Sequence

from dnaio import SequenceRecord
from cutadapt.adapters import (
    FrontAdapter,
    BackAdapter,
    PrefixAdapter,
    SuffixAdapter,
    AnywhereAdapter,
    BackAdapterStatistics,
    Adapter,
    LinkedAdapter,
)
from cutadapt.modifiers import AdapterCutter, ModificationInfo

# from .align import (
#     EndSkip,
#     Aligner,
#     PrefixComparer,
#     SuffixComparer,
#     edit_environment,
#     hamming_sphere,
# )


def test_statistics() -> None:
    read = SequenceRecord("name", "AAAACCCCAAAA")
    # Adapter 可以多个
    adapters: Sequence[Adapter] = [BackAdapter("CCCC", max_errors=0.1)]
    cutter = AdapterCutter(adapters, times=3)
    x=cutter(read, ModificationInfo(read))
    #print(x)
    # print(cutter.adapter_statistics[adapters[0]]) 
    # SingleAdapterStatistics(name=1, 
    #    end=EndStatistics(max_error_rate=0.1, errors={8: {0: 1}}, adjacent_bases={'A': 1, 'C': 0, 'G': 0, 'T': 0, '': 0})
    #     )
    assert isinstance(cutter.adapter_statistics[adapters[0]], BackAdapterStatistics)
    lengths = cutter.adapter_statistics[adapters[0]].end.lengths
    trimmed_bp = sum(seqlen * count for (seqlen, count) in lengths.items())
    print(trimmed_bp,lengths)
    assert trimmed_bp <= len(read), trimmed_bp

def test_anywhere_with_errors():
    adapter = AnywhereAdapter("CCGCATTTAG", max_errors=0.1)
    for seq, expected_trimmed in (
        ("AACCGGTTccgcatttagGATC", "AACCGGTT"),
        ("AACCGGTTccgcgtttagGATC", "AACCGGTT"),  # one mismatch
        ("AACCGGTTccgcatttag", "AACCGGTT"),
        ("ccgcatttagAACCGGTT", "AACCGGTT"),
        ("ccgtatttagAACCGGTT", "AACCGGTT"),  # one mismatch
        ("ccgatttagAACCGGTT", "AACCGGTT"),  # one deletion
    ):
        read = SequenceRecord("foo", seq)
        cutter = AdapterCutter([adapter], times=1)
        trimmed_read = cutter(read, ModificationInfo(read))
        print(trimmed_read.sequence,expected_trimmed,read.sequence)
        assert trimmed_read.sequence == expected_trimmed
#test_anywhere_with_errors()

def test_end_trim_with_mismatch():
    """
    Test the not-so-obvious case where an adapter of length 13 is trimmed from
    the end of a sequence with overlap 9 and there is one deletion.
    In this case the algorithm starts with 10 bases of the adapter to get
    the hit and so the match is considered good. An insertion or substitution
    at the same spot is not a match.
    """
    adapter = BackAdapter("TCGATCGATCGAT", max_errors=0.1)

    read = SequenceRecord("foo1", "AAAAAAAAAAATCGTCGATC")
    cutter = AdapterCutter([adapter], times=1)
    trimmed_read = cutter(read, ModificationInfo(read))
    print(trimmed_read)
    assert trimmed_read.sequence == "AAAAAAAAAAA"
    assert cutter.adapter_statistics[adapter].end.lengths == {9: 1}
    # We see 1 error at length 9 even though the number of allowed mismatches at
    # length 9 is 0.
    assert cutter.adapter_statistics[adapter].end.errors[9][1] == 1

    read = SequenceRecord("foo2", "AAAAAAAAAAATCGAACGA")
    cutter = AdapterCutter([adapter], times=1)
    trimmed_read = cutter(read, ModificationInfo(read))
    print(trimmed_read)

    assert trimmed_read.sequence == read.sequence
    assert cutter.adapter_statistics[adapter].end.lengths == {}

#test_end_trim_with_mismatch()


def test_prefix_match_with_n_wildcard_in_read():
    adapter = PrefixAdapter("NNNACGT", indels=False)
    match = adapter.match_to("TTTACGTAAAA")
    assert match is not None and (0, 7) == (match.rstart, match.rstop)
    match = adapter.match_to("NTTACGTAAAA")
    assert match is not None and (0, 7) == (match.rstart, match.rstop)

test_prefix_match_with_n_wildcard_in_read()
# 类
# class FrontAdapter(SingleAdapter):
#     """A 5' adapter"""

#     description = "regular 5'"

# class BackAdapter(SingleAdapter):
#     """A 3' adapter"""

#     description = "regular 3'"


# class AnywhereAdapter(SingleAdapter):
#     """
#     An adapter that can be 5' or 3'. If a match involves the first base of
#     the read, it is assumed to be a 5' adapter and a 3' otherwise.
#     """

#     description = "variable 5'/3'"

# class PrefixAdapter(NonInternalFrontAdapter):
#     """An anchored 5' adapter"""

#     description = "anchored 5'"

# class SuffixAdapter(NonInternalBackAdapter):
#     """An anchored 3' adapter"""
#     description = "anchored 3'"

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

# class SingleAdapter(Adapter, ABC):
#     """
#     This class is used to find a single adapter characterized by sequence, error rate,
#     type etc. within reads.

#     Arguments:
#         sequence (str): The adapter sequence. Will be converted to uppercase.
#             Also, Us will be converted to Ts.

#         max_errors: Maximum allowed errors (non-negative float). If the values is less than 1, this
#             is interpreted as a rate and passed to the aligner. If it is 1 or greater, the value
#             is converted to a rate by dividing it by the number of non-N characters in the sequence.

#         The error rate is the number of errors in the alignment divided by the length
#         of the part of the alignment that matches the adapter.

#         min_overlap: Report a match only if at least this number of bases of the adapter are
#             aligned to the read.

#         read_wildcards: Whether IUPAC wildcards in the read are allowed.

#         adapter_wildcards: Whether IUPAC wildcards in the adapter are allowed.

#         name: Optional name of the adapter. If not provided, the name is set to a
#             unique number.

#         indels: Whether indels are allowed in the alignment.
#     """

#     allows_partial_matches: bool = True

#     def __init__(
#         self,
#         sequence: str,
#         max_errors: float = 0.1,
#         min_overlap: int = 3,
#         read_wildcards: bool = False,
#         adapter_wildcards: bool = True,
#         name: Optional[str] = None,
#         indels: bool = True,
#             ):
#         pass


    
front_adapter = FrontAdapter(
                             sequence="TCGA", 
                             max_errors=0.3,
                             min_overlap=4,
                             read_wildcards=False, #N
                             adapter_wildcards=False, #N
                             indels=True
                             )

back_adapter = BackAdapter("TCGA", max_errors=0.3, min_overlap=4)
# PrefixAdapter # 非内部接头，自定义，只匹配最开头出现的
# SuffixAdapter # 非内部接头，自定义，只匹配末端出现的
# FrontAdapter  # 接头前测的一并注释为接头 # RemoveBeforeMatch
# BackAdapter   # 接头后侧的一并注释为接头 # RemoveAfterMatch
# AnywhereAdapter # 任何位置都可以搜索，先搜5’前面，后缩后面
adapter_seq = "ACCGTT".upper()
adapter = AnywhereAdapter(
                            sequence=adapter_seq, #RemoveAfterMatch
                            max_errors=0.5,
                            min_overlap=4,
                            read_wildcards=False, #N
                            adapter_wildcards=False, #N
                            indels=True
                            )
'''
AACCGGTTCTGXXXXXXXXXXXTCATCGGTAGCAGGAA
           
'''
seq='AACCGGTTccgcatttagGATC'.upper()
print(seq)
print(adapter_seq)
result = adapter.match_to(seq)
#adapter        #RemoveBeforeMatch(astart=0, astop=4, rstart=0, rstop=4, score=4, errors=0) # 坐标都是 0-base
# front_adapter #RemoveBeforeMatch(astart=0, astop=4, rstart=0, rstop=4, score=4, errors=0)
# back_adapter  #RemoveAfterMatch (astart=0, astop=4, rstart=0, rstop=4, score=4, errors=0)
print(result)

read = SequenceRecord("foo", seq)
print(read)
cutter = AdapterCutter([adapter], times=2,action='lowercase')
trimmed_read = cutter(read, ModificationInfo(read))
print(trimmed_read)

############################# alignment ####################

# PrefixComparer(
#                 self.sequence,
#                 self.max_error_rate,
#                 wildcard_ref=self.adapter_wildcards,
#                 wildcard_query=self.read_wildcards,
#                 min_overlap=self.min_overlap,
#             )


# def _make_aligner(self, sequence: str, flags: int) -> Aligner:
#     # TODO
#     # Indels are suppressed by setting their cost very high, but a different algorithm
#     # should be used instead.
#     indel_cost = 1 if self.indels else 100000
#     return Aligner(
#         sequence,
#         self.max_error_rate,
#         flags=flags,
#         wildcard_ref=self.adapter_wildcards,
#         wildcard_query=self.read_wildcards,
#         indel_cost=indel_cost,
#         min_overlap=self.min_overlap,
#     )



# def match_to(self, sequence: str):
#     """
#     Attempt to match this adapter to the given string.

#     Return a Match instance if a match was found;
#     return None if no match was found given the matching criteria (minimum
#     overlap length, maximum error rate).
#     """
#     if not self.kmer_finder.kmers_present(sequence):
#         return None
#     alignment = self.aligner.locate(sequence.upper())
#     if self._debug:
#         print(self.aligner.dpmatrix)
#     if alignment is None:
#         return None
#     # guess: if alignment starts at pos 0, it’s a 5' adapter
#     if alignment[2] == 0:  # index 2 is rstart
#         match = RemoveBeforeMatch(*alignment, adapter=self, sequence=sequence)  # type: ignore
#     else:
#         match = RemoveAfterMatch(*alignment, adapter=self, sequence=sequence)  # type: ignore
#     return match

# match = self.adapters.match_to(trimmed_read.sequence)

# def _aligner(self):
#     return self._make_aligner(self.sequence, Where.ANYWHERE.value)

def compare_prefixes(ref, query, wildcard_ref=False, wildcard_query=False):
    aligner = PrefixComparer(
        ref,
        max_error_rate=0.9,
        wildcard_ref=wildcard_ref,
        wildcard_query=wildcard_query,
    )
    return aligner.locate(query)



# class RemoveBeforeMatch(SingleMatch):
#     """A match that removes sequence before the match"""

#     def rest(self) -> str:
#         """
#         Return the part of the read before this match if this is a
#         'front' (5') adapter,
#         return the part after the match if this is not a 'front' adapter (3').
#         This can be an empty string.
#         """
#         return self.sequence[: self.rstart]

#     def remainder_interval(self) -> Tuple[int, int]:
#         """
#         Return an interval (start, stop) that describes the part of the read that would
#         remain after trimming
#         """
#         return self.rstop, len(self.sequence)

#     def retained_adapter_interval(self) -> Tuple[int, int]:
#         return self.rstart, len(self.sequence)

#     def trim_slice(self):
#         # Same as remainder_interval, but as a slice() object
#         return slice(self.rstop, None)

#     def trimmed(self, read):
#         return read[self.rstop :]

#     def removed_sequence_length(self) -> int:
#         return self.rstop


# class RemoveAfterMatch(SingleMatch):
#     """A match that removes sequence after the match"""

#     def rest(self) -> str:
#         """
#         Return the part of the read before this match if this is a
#         'front' (5') adapter,
#         return the part after the match if this is not a 'front' adapter (3').
#         This can be an empty string.
#         """
#         return self.sequence[self.rstop :]

#     def remainder_interval(self) -> Tuple[int, int]:
#         """
#         Return an interval (start, stop) that describes the part of the read that would
#         remain after trimming
#         """
#         return 0, self.rstart

#     def retained_adapter_interval(self) -> Tuple[int, int]:
#         return 0, self.rstop

#     def trim_slice(self):
#         # Same as remainder_interval, but as a slice() object
#         return slice(None, self.rstart)

#     def trimmed(self, read):
#         return read[: self.rstart]

#     def adjacent_base(self) -> str:
#         return self.sequence[self.rstart - 1 : self.rstart]

#     def removed_sequence_length(self) -> int:
#         return len(self.sequence) - self.rstart






# class LinkedAdapter(Adapter):
#     """A 5' adapter combined with a 3' adapter"""

#     description = "linked"
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
    
def test_linked_adapter_statistics():
    # Issue #615
    front_adapter = PrefixAdapter("GGG") #可以详细设置，因为front_required=True, 所以使用的是PrefixAdapter，而不是FrontAdapter，全部位置匹配
    back_adapter = BackAdapter("ACGACGACGACG")
    la = LinkedAdapter(
        front_adapter,
        back_adapter,
        front_required=True,
        back_required=False,
        name="name",
    )
    statistics = la.create_statistics()
    match = la.match_to("GGGTTTTTACGACTACGACG")
    #print(match)
    '''
    <LinkedMatch(front_match=RemoveBeforeMatch(astart=0, astop=3, rstart=0, rstop=3, score=3, errors=0), back_match=RemoveAfterMatch(astart=0, astop=12, rstart=5, rstop=17, score=10, errors=1), adapter=LinkedAdapter(front_adapter=<PrefixAdapter(name='name', sequence='GGG', max_error_rate=0.1, min_overlap=3, read_wildcards=False, adapter_wildcards=False, indels=True)>, back_adapter=<BackAdapter(name='2', sequence='ACGACGACGACG', max_error_rate=0.1, min_overlap=3, read_wildcards=False, adapter_wildcards=False, indels=True)>))>
    print(match.front_match)
    print(match.back_match)
    '''
    statistics.add_match(match)

    front, back = statistics.end_statistics()
    
    #print(front)
    #print(back)
    '''
    EndStatistics(max_error_rate=0.1, errors={3: {0: 1}}, adjacent_bases={'A': 0, 'C': 0, 'G': 0, 'T': 0, '': 0})
    EndStatistics(max_error_rate=0.1, errors={12: {1: 1}}, adjacent_bases={'A': 0, 'C': 0, 'G': 0, 'T': 1, '': 0})
    '''
    assert back.errors.get(12) == {1: 1}
    assert front.errors.get(3) == {0: 1}


def test_linked_matches_property():
    """Accessing matches property of non-anchored linked adapters"""
    # Issue #265
    front_adapter = FrontAdapter("GGG")
    back_adapter = BackAdapter("TTT")
    la = LinkedAdapter(
        front_adapter,
        back_adapter,
        front_required=False,
        back_required=False,
        name="name",
    )
    assert la.match_to("AAAATTTT").score == 3

# # TODO remove this enum, this should be within each Adapter class
# class Where(IntFlag):
#     """
#     Aligner flag combinations for all adapter types.

#     "REFERENCE" is the adapter sequence, "QUERY" is the read sequence
#     """

#     BACK = EndSkip.QUERY_START | EndSkip.QUERY_STOP | EndSkip.REFERENCE_END
#     FRONT = EndSkip.QUERY_START | EndSkip.QUERY_STOP | EndSkip.REFERENCE_START
#     PREFIX = EndSkip.QUERY_STOP
#     SUFFIX = EndSkip.QUERY_START
#     # Just like FRONT/BACK, but without internal matches
#     FRONT_NOT_INTERNAL = EndSkip.REFERENCE_START | EndSkip.QUERY_STOP
#     BACK_NOT_INTERNAL = EndSkip.QUERY_START | EndSkip.REFERENCE_END
#     ANYWHERE = EndSkip.SEMIGLOBAL

test_linked_adapter()
