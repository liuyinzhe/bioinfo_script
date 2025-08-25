# Install MCR(MATLAB_Runtime)

```bash
mkdir MATLAB_Runtime_R2019b_Update_9_glnxa64
cd MATLAB_Runtime_R2019b_Update_9_glnxa64
wget https://ssd.mathworks.com/supportfiles/downloads/R2019b/Release/9/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2019b_Update_9_glnxa64.zip
unzip MATLAB_Runtime_R2019b_Update_9_glnxa64.zip
./install -mode silent -agreeToLicense yes -destinationFolder /data/software/MCRROOT/v97
```

# Configure Environment Variables
>matlab_runtime.sh
```bash
export MCRROOT=/data/software/MCRROOT/v97
LD_LIBRARY_PATH=.:${MCRROOT}/runtime/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/bin/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/sys/os/glnxa64;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/extern/bin/glnxa64;
MCRJRE=${MCRROOT}/sys/java/jre/glnxa64/jre/lib/amd64 ;

LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRJRE}/server ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRJRE}/jli ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRJRE} ;
export LD_LIBRARY_PATH;
echo LD_LIBRARY_PATH is ${LD_LIBRARY_PATH};

export JAVA_HOME=/data/software/MATLAB_Runtime_R2019b_Update_9_glnxa64/sys/java/jre/glnxa64/jre
export PATH=${JAVA_HOME}/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib

echo MCRROOT is ${MCRROOT}
```


# clone 5R
```bash
git clone https://github.com/NoamShental/5R.git
```
# run shell
>run.sh
```bash
mkdir example_results
/data/software/5R/5R_linux/run_main_5R.sh  \
  /data/software/MCRROOT/v97 \
  /data/test/5R/example_fastq \
  /data/software/5R/GG_5R \
  GreenGenes_201305 \
  /data/test/5R/example_results/5R_SMURF_example.txt \
  126 
```
