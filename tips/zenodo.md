
### install zenodo_get
```
pip install zenodo_get
```
### example
```bash
# https://doi.org/10.5281/zenodo.10457005
# DOI: 10.5281/zenodo.10457006
/data/software/miniconda3/bin/zenodo_get -r 10457005 # Download error.
/data/software/miniconda3/bin/zenodo_get -d 10.5281/zenodo.10457006 # 可以下载
```
### 无法访问zenodo.org解决
>> 上面zenodo_get 也会遇到 Download error.
#### 1.站长之家查网站ip
>https://ip.tool.chinaz.com/zenodo.org
>>188.185.48.194
#### 2.修改hosts
>C:\WINDOWS\system32\drivers\etc\hosts
>右键-属性-安全选项卡-选取当前用户-编辑-完全控制-应用
>添加:188.185.48.194 zenodo.org
