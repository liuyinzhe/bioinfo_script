

# pip install SigProfilerExtractor
# from SigProfilerMatrixGenerator import install as genInstall

# download genome
# genInstall.install('GRCh37', bash=True)
# genInstall.install('GRCh37', rsync=False, bash=True)
# genInstall.install('GRCh38') 


# Mutational Signatures 吗？
# Single Base Substitution (SBS) Signatures

from pathlib import Path
from SigProfilerMatrixGenerator.scripts import SigProfilerMatrixGeneratorFunc as matGen


def main():
    # 执行目录
    pwd  = Path().cwd()
    # 参考基因组
    reference_genome = "GRCh37"

    # Signatures分析
    
    # 设置 vcf 路径 # 注意，不能包含其它任何文件，会影响绘图
    vcf_dir = pwd.joinpath("vcf")
    
    matrices = matGen.SigProfilerMatrixGeneratorFunc(project="SBS",reference_genome=reference_genome,path_to_input_files=str(vcf_dir), plot=True)
    #matrices = matGen.SigProfilerMatrixGeneratorFunc(project="Single Base Substitution",reference_genome=reference_genome,path_to_input_files='/mnt/d/刘银喆/阅微/project/个性化/MutationalPatterns/20240819', plot=True)
    #matrices = matGen.SigProfilerMatrixGeneratorFunc("PC_67_PC65.snp.vcf", reference_genome, './', plot=True)
    '''

    matrices = matGen.SigProfilerMatrixGeneratorFunc("temp",
    "GRCh38", "./", plot=True,exome=False,bed_file=None,
    chrom_based=False,tsb_stat=False,seqInfo=False,cushion=100)

    参数说明：
    project: 项目名称，生成结果的文件名前缀
    reference_genome: 参考基因组名称
    path_to_input_files: 输入文件路径，也是输出路径，生成 input、logs 与 output 目录
    plot: 是否绘制分析结果
    # exome 默认False 分析全部的mutation，不只是exon
    # bed_file 默认False 无bed_file文件输入
    # chrom_based 默认False 不输出charom based的matrix
    # seqInfo 默认False 不输出原始突变序列矩阵
    # cushion 默认100 如果exome和bed_file均为False，这个参数意义也不大，是在给定位置上下游100处，统计突变

    '''

    # https://osf.io/s93d5/wiki/6.%20Quick%20Start%20Example/
    # https://chenhongyubio.github.io/2020/07/28/Mutational-Signatures%E5%88%86%E6%9E%90/


if __name__ == '__main__':
    main()

