conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda

conda config --add channels ursky

mamba create -n metawrap python=2.7  metawrap-mg
