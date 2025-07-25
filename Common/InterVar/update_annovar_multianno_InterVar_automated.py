import polars as pl
import re
import sys
from pathlib import Path
import subprocess
# line_str="InterVar: Uncertain significance PVS1="
# match_obj = re.search("InterVar: (.*?) PVS1",line_str)
# print(match_obj.group(1))

def runshell(command):
    return_obj =subprocess.run(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               check=True,encoding=None,timeout=None)
    returncode = return_obj.returncode
    return returncode

def main():
    '''
    platform: Linux 
    python test.py  sample.snp.hg38_multianno.txt
    '''
    script_path = Path(__file__)
    scripts_dir = Path(script_path).parent
    current_dir = Path.cwd()


    multianno_file_path = Path(sys.argv[1])
    intervar_file_path = multianno_file_path.with_suffix(".txt.intervar")
    #multianno_file = sys.argv[1] # "sample.snp.hg38_multianno.txt"
    #pl_df = pl.scan_csv(multianno_file+".intervar",separator="\t",infer_schema=False)\
    pl_df = pl.scan_csv(intervar_file_path,separator="\t",infer_schema=False)\
    .select(["#Chr","Start","End","Ref","Alt"," InterVar: InterVar and Evidence "]).collect()
    print(pl_df.columns) # list
    print(pl_df)

    #[row["b"] for row in df.iter_rows(named=True)]

    #intervar_set = set()
    intervar_dic = {}
    for row in pl_df.iter_rows(named=True):
        chrom = row["#Chr"]
        start = row["Start"]
        end = row["End"]
        ref_base = row["Ref"]
        alt_base = row["Alt"]
        raw_intervar = row[" InterVar: InterVar and Evidence "]
        '''
        InterVar: Benign PVS1=0
        InterVar: Likely benign PVS1=0
        InterVar: Uncertain significance PVS1=0
        '''
        intervar = re.search("InterVar: (.*?) PVS1",raw_intervar).group(1)
        # intervar_set.add(intervar)
        key_str ="\t".join([chrom,start,end,ref_base,alt_base])
        if key_str not in intervar_dic:
            intervar_dic[key_str] = intervar
        else:
            if intervar_dic[key_str] != intervar:
                intervar_dic[key_str] = ';'.join([intervar_dic[key_str],intervar])
    # print(intervar_set)

    # # 只读第一行获取原始header # 由于header中存在重复内容,不能用pandas和polars 读取会添加_duplicated_{index}
    header_path = multianno_file_path.parent.joinpath("header")
    command_head = "head -n 1 {input} > {header}".format(input=multianno_file_path,header=header_path)
    returncode = runshell(command_head)
    if returncode != 0:
        print("head err")
        exit(1)

    # 读取CSV文件
    multianno_df = pl.read_csv(multianno_file_path,separator="\t",infer_schema=False,truncate_ragged_lines=True)# 保持原始名字


    # 创建映射DataFrame #从Python 3.7开始,字典的插入顺序被保留,因此keys()和values()的顺序是插入的顺序，并且两个方法返回的对应顺序是一致的
    mapping_df = pl.DataFrame({
        "key": list(intervar_dic.keys()),
        "replacement": list(intervar_dic.values())
    })

    # # 使用字典的 items() 方法 # 3.6 及以前版本键值对每次都是不同的
    # mapping_df = pl.DataFrame(
    #     data=list(intervar_dic.items()),
    #     schema=["key", "replacement"]
    # )

    # 处理流程
    result = (
        multianno_df
        # 1. 创建组合键列
        .with_columns(
            key=pl.concat_str(
                [pl.col("Chr"), pl.col("Start"), pl.col("End"),pl.col("Ref"),pl.col("Alt")],
                separator="_"
            )
        )
        # 2. 左连接映射表
        .join(
            mapping_df,
            on="key",
            how="left"
        )
        # 3. 替换目标列
        .with_columns(
            InterVar_automated=pl.coalesce( #使用coalesce(优先使用new_value,如果为null则使用原列)更新InterVar_automated列
                pl.col("replacement"),
                pl.col("InterVar_automated")
            )
        )
        # 4. 清理临时列
        .drop(["key", "replacement"])
    )

    # 查看结果
    print(result)

    # 保存结果(如果需要)
    result.write_csv(multianno_file_path,separator="\t")

    # 恢复原始列名
    # result = result.rename(dict(zip(result.columns, original_headers)))

    sed_command = '''sed -i "1s/^.*$/$(sed 's/[\/&]/\\&/g' {header_file} )/" {multianno_file}'''.format(header_file=header_path,multianno_file=multianno_file_path)
    returncode = runshell(sed_command)
    if returncode != 0:
        print("sed err")
        exit(1)

if __name__ == "__main__":
    main()
