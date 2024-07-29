# oge-api-python

- 构建wheel

```shell
python setup.py clean --all
python setup.py bdist_wheel
```

whl文件位于dist目录下

- 安装依赖项

```shell
pip install ./dist/oge-{version}-py3-none-any.whl six requests
```
# 说明
1. oge的algorithms.json文件的同步目前通过计算端项目进行同步。该仓库的algorithms.json文件现已停止维护。
2. 为了功能稳定，现在的oge的algorithms.json文件解析通过硬编码指定路径在本地读取。代码参考oge/data.py中的：
```python
fileLocation = "/mnt/algorithms.json"
```