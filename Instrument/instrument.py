# https://github.com/10XGenomics/supernova/blob/master/tenkit/lib/python/tenkit/illumina_instrument.py
# dictionary of instrument id regex: [platform(s)]
InstrumentIDs = {"HWI-M[0-9]{4}$" : ["MiSeq"],
        "HWUSI" : ["Genome Analyzer IIx"],
        "M[0-9]{5}$" : ["MiSeq"],
        "HWI-C[0-9]{5}$" : ["HiSeq 1500"],
        "C[0-9]{5}$" : ["HiSeq 1500"],
        "HWI-D[0-9]{5}$" : ["HiSeq 2500"],
        "D[0-9]{5}$" : ["HiSeq 2500"],
        "J[0-9]{5}$" : ["HiSeq 3000"],
        "K[0-9]{5}$" : ["HiSeq 3000","HiSeq 4000"],
        "E[0-9]{5}$" : ["HiSeq X"],
        "NB[0-9]{6}$": ["NextSeq"],
        "NS[0-9]{6}$" : ["NextSeq"],
        "MN[0-9]{5}$" : ["MiniSeq"]}

# dictionary of flow cell id regex: ([platform(s)], flow cell version and yeild)
FCIDs = {"C[A-Z,0-9]{4}ANXX$" : (["HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v4 flow cell"),
         "C[A-Z,0-9]{4}ACXX$" : (["HiSeq 1000", "HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v3 flow cell"),
         "H[A-Z,0-9]{4}ADXX$" : (["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v1 flow cell"),
         "H[A-Z,0-9]{4}BCXX$" : (["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"),
         "H[A-Z,0-9]{4}BCXY$" : (["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"),
         "H[A-Z,0-9]{4}BBXX$" : (["HiSeq 4000"], "(8-lane) v1 flow cell"),
         "H[A-Z,0-9]{4}BBXY$" : (["HiSeq 4000"], "(8-lane) v1 flow cell"),
         "H[A-Z,0-9]{4}CCXX$" : (["HiSeq X"], "(8-lane) flow cell"),
         "H[A-Z,0-9]{4}CCXY$" : (["HiSeq X"], "(8-lane) flow cell"),
         "H[A-Z,0-9]{4}ALXX$" : (["HiSeq X"], "(8-lane) flow cell"),
         "H[A-Z,0-9]{4}BGXX$" : (["NextSeq"], "High output flow cell"),
         "H[A-Z,0-9]{4}BGXY$" : (["NextSeq"], "High output flow cell"),
         "H[A-Z,0-9]{4}BGX2$" : (["NextSeq"], "High output flow cell"),
         "H[A-Z,0-9]{4}AFXX$" : (["NextSeq"], "Mid output flow cell"),
         "A[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq flow cell"),
         "B[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq flow cell"),
         "D[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq nano flow cell"),
         "G[A-Z,0-9]{4}$" : (["MiSeq"], "MiSeq micro flow cell"),
         "H[A-Z,0-9]{4}DMXX$" : (["NovaSeq"], "S2 flow cell")}

# other 
# NovaSeq X Plus 
# instrument id: LH00308
# flow cell id: 227VVLLT4
