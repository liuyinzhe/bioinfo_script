# Mapping ONT or PacBio-hifi WGS reads

meryl count k=15 output merylDB ref.fa
meryl print greater-than distinct=0.9998 merylDB > repetitive_k15.txt

winnowmap -W repetitive_k15.txt -L --MD -Y -ax map-ont ref.fa ont.fq.gz > output.sam
#winnowmap -W repetitive_k15.txt -L --MD -Y -ax map-pb ref.fa hifi.fq.gz > output.sam



# Mapping genome assemblies

meryl count k=19 output merylDB asm1.fa
meryl print greater-than distinct=0.9998 merylDB > repetitive_k19.txt

winnowmap -W repetitive_k19.txt -ax asm20 asm1.fa asm2.fa > output.sam
