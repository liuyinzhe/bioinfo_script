conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda

conda config --add channels ursky

mamba create -n metawrap python=2.7  metawrap-mg

#modify
#/envs/metawrap/bin/config-metawrap

# bug : metawrap  --show-config
# ImportError: No module named _sysconfigdata_x86_64_conda_linux_gnu
cp -a /data/xx/miniconda3/pkgs/python-2.7/lib/python2.7/_sysconfigdata_x86_64_conda_linux_gnu.py* /data/yy/miniconda3/envs/metawrap/lib/python2.7/
