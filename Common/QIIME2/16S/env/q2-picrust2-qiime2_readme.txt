#https://library.qiime2.org/plugins/picrust/q2-picrust2

#conda env create --name q2-picrust2-qiime2-2024.5 --file https://raw.githubusercontent.com/picrust/q2-picrust2/refs/heads/master/environment-files/q2-picrust2-qiime2-amplicon-2024.5.yml
#conda env update --file https://raw.githubusercontent.com/picrust/q2-picrust2/refs/heads/master/environment-files/q2-picrust2-qiime2-amplicon-2024.5.yml

#https://github.com/picrust/picrust2/wiki/q2-picrust2-Tutorial/

nohup  conda env create -y --name q2-picrust2-qiime2 --file https://raw.githubusercontent.com/picrust/q2-picrust2/refs/heads/master/environment-files/q2-picrust2-qiime2-amplicon-2024.5.yml &


# To activate this environment, use
#
#     $ conda activate q2-picrust2-qiime2
#
# To deactivate an active environment, use
#
#     $ conda deactivate
