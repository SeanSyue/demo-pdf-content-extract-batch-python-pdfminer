"""
https://zhuanlan.zhihu.com/p/34819237
https://github.com/wshuyi/demo-pdf-content-extract-batch-python-pdfminer
分析流程整理成函数，以便于将来更方便地调用
"""
import glob
from pdf_extractor import extract_pdf_content
import pandas as pd
import matplotlib.pyplot as plt

# 获得所有 pdf 文件的路径
pdf_path = "pdf/"
pdfs = glob.glob("{}/*.pdf".format(pdf_path))
print(pdfs)

# 从 pdf 文件列表中的第一篇里，抽取内容
content = extract_pdf_content(pdfs[0])
print(content)

# 建立辞典，批量抽取和存储内容
# 遍历 `pdfs` 列表，把文件名称（不包含目录）作为键值
mydict = {}
for pdf in pdfs:
    key = pdf.split('/')[-1]
    if key not in mydict:
        print("Extracting content from {} ...".format(pdf))  # 为了让这个过程更为清晰，我们让Python输出正在抽取的 pdf 文件名
        mydict[key] = extract_pdf_content(pdf)
print(mydict.keys())


# 字典变成数据框，以利于分析
# 注意后面的`reset_index()`把原先字典键值生成的索引也转换成了普通的列
df = pd.DataFrame.from_dict(mydict, orient='index').reset_index()
df.columns = ["path", "content"]  # 重新命名列，以便于后续使用
print(df)

# 统计抽取内容的长度
# 多出的一列，就是 pdf 文本内容的字符数量
df["length"] = df.content.apply(lambda x: len(x))
print(df)

# %matplotlib inline
plt.figure(figsize=(14, 6))  # 设置了图片的长宽比例
df.set_index('path').length.plot(kind='bar')
plt.xticks(rotation=45)  # 对应的pdf文件名称以倾斜45度来展示
plt.show()
